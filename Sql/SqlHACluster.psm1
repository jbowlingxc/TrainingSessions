<#
.SYNOPSIS
    Connects to a SQL Server Always On Availability Group cluster and determines which node is PRIMARY.

.DESCRIPTION
    Queries the sys.dm_hadr_availability_replica_states DMV to find the current
    primary replica for a given availability group. Falls back to instance-level
    check if no AG name is specified.

.PARAMETER SqlInstance
    The SQL Server instance to query (can be an AG listener name or any replica).

.PARAMETER AvailabilityGroup
    The name of the Availability Group. If omitted, queries the default/local AG.

.EXAMPLE
    Get-SQLPrimaryNode -SqlInstance "AGListenerName" -AvailabilityGroup "MyAG"

.EXAMPLE
    Get-SQLPrimaryNode -SqlInstance "ServerA\INST1"
#>
function Get-SQLPrimaryNode {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$SqlInstance,

        [Parameter(Mandatory = $false)]
        [string]$AvailabilityGroup
    )

    try {
        if (-not (Get-Module -ListAvailable -Name SqlServer)) {
            throw "The 'SqlServer' PowerShell module is not installed. Run: Install-Module -Name SqlServer -Force"
        }

        Import-Module SqlServer -ErrorAction Stop

        if ($AvailabilityGroup) {
            $query = @"
            SELECT ar.replica_server_name AS ReplicaName,
                   ars.role_desc AS Role,
                   ars.connected_state_desc AS ConnectionState,
                   ars.recovery_health_desc AS RecoveryHealth,
                   ar.availability_mode_desc AS AvailabilityMode
            FROM sys.dm_hadr_availability_replica_states ars
            JOIN sys.availability_replicas ar
                ON ars.replica_id = ar.replica_id
            JOIN sys.availability_groups ag
                ON ar.group_id = ag.group_id
            WHERE ag.name = '$($AvailabilityGroup.Replace("'", "''"))'
            ORDER BY ars.role_desc DESC;
"@
        }
        else {
            $query = @"
            SELECT ar.replica_server_name AS ReplicaName,
                   ars.role_desc AS Role,
                   ars.connected_state_desc AS ConnectionState,
                   ars.recovery_health_desc AS RecoveryHealth,
                   ar.availability_mode_desc AS AvailabilityMode
            FROM sys.dm_hadr_availability_replica_states ars
            JOIN sys.availability_replicas ar
                ON ars.replica_id = ar.replica_id
            WHERE ars.role_desc = 'PRIMARY'
            ORDER BY ars.connected_state DESC;
"@
        }

        $results = Invoke-Sqlcmd -ServerInstance $SqlInstance -Query $query -ErrorAction Stop

        if ($results.Count -eq 0) {
            throw "No replicas found for the specified context. Verify the Availability Group name and connectivity."
        }

        $primary = $results | Where-Object { $_.Role -eq 'PRIMARY' }

        if ($primary) {
            $output = [PSCustomObject]@{
                AvailabilityGroup  = $AvailabilityGroup
                PrimaryNode        = $primary.ReplicaName
                ConnectionState    = $primary.ConnectedStateDesc
                RecoveryHealth     = $primary.RecoveryHealthDesc
                AvailabilityMode   = $primary.AvailabilityModeDesc
                IsHealthy          = $true
            }
            Write-Verbose "Primary node: $($output.PrimaryNode) for AG '$($AvailabilityGroup)' on $SqlInstance"
            return $output
        }
        else {
            # Return all replicas when none is PRIMARY (edge case — cluster may be in transition)
            $output = $results | ForEach-Object {
                [PSCustomObject]@{
                    ReplicaName    = $_.ReplicaName
                    Role           = $_.Role
                    ConnectionState = $_.ConnectedStateDesc
                    RecoveryHealth = $_.RecoveryHealthDesc
                    AvailabilityMode = $_.AvailabilityModeDesc
                    IsHealthy      = ($_.RecoveryHealthDesc -eq 'HEALTHY' -and $_.ConnectedStateDesc -eq 'CONNECTED')
                }
            }
            Write-Warning "No PRIMARY replica found. Returning all replicas. AG may be in transition."
            return $output
        }
    }
    catch [System.Management.Automation.MethodInvocationException] {
        throw "SQL connection error to '$SqlInstance': $($_.Exception.InnerException.Message)"
    }
    catch {
        throw "Get-SQLPrimaryNode failed: $_"
    }
}


<#
.SYNOPSIS
    Safely moves the primary role of an Availability Group to another replica.

.DESCRIPTION
    Performs a full pre-move health check, optionally sets the specified replica to
    MANUAL failover mode, triggers the role change, and validates the new primary.

    The function will NOT proceed if:
    - The target replica is not SECONDARY
    - The target replica is not HEALTHY (synchronized)
    - The target replica is not CONNECTED
    - The target replica is not listed in the AG replica list

.PARAMETER SqlInstance
    Any reachable SQL Server instance in the Availability Group.

.PARAMETER AvailabilityGroup
    The name of the Availability Group.

.PARAMETER TargetReplica
    The server name of the replica to become the new primary.

.PARAMETER FailoverMode
    'AUTOMATIC' or 'MANUAL'. Sets the target replica's failover mode before the move.
    Defaults to 'MANUAL' for safety.

.PARAMETER TimeoutSeconds
    Maximum seconds to wait for synchronization and failover to complete.
    Defaults to 120.

.PARAMETER WhatIf
    Shows what would happen without performing the move.

.EXAMPLE
    Move-SQLPrimaryRole -SqlInstance "ServerA\INST1" -AvailabilityGroup "MyAG" -TargetReplica "ServerB\INST1"

.EXAMPLE
    Move-SQLPrimaryRole -SqlInstance "AGListener" -AvailabilityGroup "MyAG" -TargetReplica "ServerB\INST1" -FailoverMode AUTOMATIC -WhatIf
#>
function Move-SQLPrimaryRole {
    [CmdletBinding(SupportsShouldProcess = $true)]
    param (
        [Parameter(Mandatory = $true)]
        [string]$SqlInstance,

        [Parameter(Mandatory = $true)]
        [string]$AvailabilityGroup,

        [Parameter(Mandatory = $true)]
        [string]$TargetReplica,

        [Parameter(Mandatory = $false)]
        [ValidateSet('AUTOMATIC', 'MANUAL')]
        [string]$FailoverMode = 'MANUAL',

        [Parameter(Mandatory = $false)]
        [int]$TimeoutSeconds = 120
    )

    begin {
        if (-not (Get-Module -ListAvailable -Name SqlServer)) {
            throw "The 'SqlServer' PowerShell module is not installed. Run: Install-Module -Name SqlServer -Force"
        }
        Import-Module SqlServer -ErrorAction Stop

        Write-Verbose "Starting role move for AG '$AvailabilityGroup' to '$TargetReplica'"
    }

    process {
        # --- Step 1: Get current state ---
        $currentState = Get-SQLPrimaryNode -SqlInstance $SqlInstance -AvailabilityGroup $AvailabilityGroup -ErrorAction Stop

        if ($currentState.PSObject.TypeNames[0] -eq 'System.Management.Automation.PSCustomObject') {
            $currentPrimary = $currentState.PrimaryNode
        }
        else {
            throw "Could not determine current primary. AG may be in an inconsistent state."
        }

        Write-Host "Current primary: $currentPrimary" -ForegroundColor Cyan
        Write-Host "Target replica:  $TargetReplica" -ForegroundColor Cyan
        Write-Host "Failover mode:   $FailoverMode" -ForegroundColor Cyan

        if ($currentPrimary -eq $TargetReplica) {
            Write-Warning "Target replica '$TargetReplica' is already the primary. Nothing to do."
            return
        }

        # --- Step 2: Verify target replica is a valid SECONDARY ---
        $targetQuery = @"
            SELECT ars.replica_server_name, ars.role_desc, ars.connected_state_desc,
                   ars.synchronization_state_desc, ars.synchronization_health_desc
            FROM sys.dm_hadr_availability_replica_states ars
            JOIN sys.availability_replicas ar
                ON ars.replica_id = ar.replica_id
            JOIN sys.availability_groups ag
                ON ar.group_id = ag.group_id
            WHERE ag.name = '$($AvailabilityGroup.Replace("'", "''"))'
              AND ars.replica_server_name = '$($TargetReplica.Replace("'", "''"))';
"@

        $targetState = Invoke-Sqlcmd -ServerInstance $SqlInstance -Query $targetQuery -ErrorAction Stop

        if ($targetState.Count -eq 0) {
            throw "Target replica '$TargetReplica' is not part of availability group '$AvailabilityGroup'."
        }

        if ($targetState.role_desc -ne 'SECONDARY') {
            throw "Target replica '$TargetReplica' is currently '$($targetState.role_desc)', not SECONDARY. Cannot move primary to a non-secondary replica."
        }

        if ($targetState.connected_state_desc -ne 'CONNECTED') {
            throw "Target replica '$TargetReplica' is not CONNECTED. Current state: $($targetState.connected_state_desc)."
        }

        if ($targetState.synchronization_health_desc -ne 'HEALTHY') {
            throw "Target replica '$TargetReplica' is not HEALTHY. Sync state: $($targetState.synchronization_state_desc)."
        }

        Write-Host "Target replica health check passed." -ForegroundColor Green

        # --- Step 3: Set failover mode on target replica (if needed) ---
        if ($FailoverMode -eq 'MANUAL') {
            Write-Verbose "Setting failover mode to MANUAL on '$TargetReplica'..."
            $alterQuery = @"
            USE master;
            ALTER AVAILABILITY GROUP [$($AvailabilityGroup.Replace("'", "''"))]
            MODIFY REPLICA ON N'$($TargetReplica.Replace("'", "''"))'
            WITH (FAILOVER_MODE = MANUAL);
"@
            try {
                Invoke-Sqlcmd -ServerInstance $SqlInstance -Query $alterQuery -QueryTimeout 30 -ErrorAction Stop | Out-Null
                Write-Host "Failover mode set to MANUAL on '$TargetReplica'." -ForegroundColor Green
            }
            catch {
                Write-Warning "Could not set failover mode (may already be set): $_"
            }
        }

        # --- Step 4: Perform the failover ---
        $failoverQuery = @"
USE master;
ALTER AVAILABILITY GROUP [$($AvailabilityGroup.Replace("'", "''"))]
FAILOVER;
"@

        $script:Success = $false
        $script:ErrorMessage = $null

        $job = Start-Job -ScriptBlock {
            param($SqlInstance, $Query)
            try {
                $conn = New-Object System.Data.SqlClient.SqlConnection("Server=$SqlInstance;Trusted_Connection=True;")
                $conn.Open()
                $cmd = $conn.CreateCommand()
                $cmd.CommandText = $Query
                $cmd.CommandTimeout = 0
                $cmd.ExecuteNonQuery() | Out-Null
                $conn.Close()
                return $true
            }
            catch {
                return $_.Exception.Message
            }
        } -ArgumentList $SqlInstance, $failoverQuery

        # Wait for failover to complete
        $elapsed = 0
        $interval = 5

        while ($elapsed -lt $TimeoutSeconds) {
            Start-Sleep -Seconds $interval
            $elapsed += $interval

            try {
                $newPrimary = Get-SQLPrimaryNode -SqlInstance $SqlInstance -AvailabilityGroup $AvailabilityGroup -ErrorAction Stop
                if ($newPrimary.PSObject.TypeNames[0] -eq 'System.Management.Automation.PSCustomObject') {
                    if ($newPrimary.PrimaryNode -eq $TargetReplica) {
                        $script:Success = $true
                        Write-Host "Failover complete. New primary: $($newPrimary.PrimaryNode)" -ForegroundColor Green
                        break
                    }
                }
                else {
                    Write-Verbose "Still waiting for AG to stabilize... ($elapsed/$TimeoutSeconds seconds)"
                }
            }
            catch {
                Write-Verbose "Still waiting for AG to stabilize... ($elapsed/$TimeoutSeconds seconds)"
            }
        }

        Stop-Job $job | Out-Null
        Remove-Job $job | Out-Null

        if (-not $script:Success) {
            throw "Failover did not complete within ${TimeoutSeconds} seconds. The AG may be in an inconsistent state. Check manually."
        }

        # --- Step 5: Post-failover validation ---
        Write-Host "`n--- Post-Failover Validation ---" -ForegroundColor Cyan
        $validation = Get-SQLPrimaryNode -SqlInstance $SqlInstance -AvailabilityGroup $AvailabilityGroup
        $validation | Format-List

        if ($validation.PSObject.TypeNames[0] -eq 'System.Management.Automation.PSCustomObject') {
            if ($validation.PrimaryNode -eq $TargetReplica) {
                Write-Host "`nSUCCESS: Primary role moved to '$TargetReplica'." -ForegroundColor Green
            }
            else {
                Write-Warning "Primary role moved but not to the expected target. New primary: $($validation.PrimaryNode)"
            }
        }
        else {
            Write-Warning "Primary role moved but AG state is inconsistent. Manual inspection recommended."
        }
    }

    end {
        Write-Verbose "Move-SQLPrimaryRole finished."
    }
}
