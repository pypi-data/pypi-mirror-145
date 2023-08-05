# tfe-run-wait
Command line utility to poll for a Terraform Enterprise run state change and apply a planned run.

## Usage
```
tfe-run-wait [-h] \
        --token TOKEN \
        --organization ORGANIZATION \
        --clone-url CLONE_URL \
        --commit-sha COMMIT_SHA \
        [--branch BRANCH ] \
        [--workspace WORKSPACE] \
        [--wait-for-status WAIT_FOR_STATUS] \
        [--maximum-wait-time MAXIMUM_WAIT_TIME]

tfe-run-apply [-h] \
        --token TOKEN \
        --organization ORGANIZATION \
        --clone-url CLONE_URL \
        --commit-sha COMMIT_SHA \
        [--branch BRANCH ] \
        --comment COMMENT \
        [--confirm] \
        [--workspace WORKSPACE] \
        [--maximum-wait-time MAXIMUM_WAIT_TIME]
```

## Options
```
  --token TOKEN         Terraform Enterprise access token, default from TFE_API_TOKEN
  --organization ORGANIZATION
                        of the workspace
  --workspace WORKSPACE
                        to inspect runs for. if not specified apply to all workspaces associated with the source repo. 
  --clone-url CLONE_URL
                        of source repository for the run
  --commit-sha COMMIT_SHA
                        of commit which initiated the run
  --branch BRANCH                        
                        of commit which initiated the run
  --wait-for-status WAIT_FOR_STATUS
                        wait state to reach, defaults to 'applied' and 'planned_and_finished'
  --maximum-wait-time MAXIMUM_WAIT_TIME
                        for state to be reached in minutes, default 45
  --confirm             requests confirmation after showing the plan. you will have to type `yes`
  --comment             to use in the apply of the planned run.
  -h, --help            show this help message and exit
```


## Description
Finds a Terraform enterpise run initiated for the specified git commit and either polls for a specific state change or apply the planned changes.

tfe-run-wait will wait until the specified status is reached. By default it will wait for the status `applied` or `planned_and_finished`. When the run 
  reaches a non specified final state, it will exit with an error.

tfe-run-apply will request terraform to apply to plan for the run. If the status of the run is already `applied` or `planned_and_finished`, it will exit without an error.
  It will not check whether the run is in the correct state. The run should be in the state `planned` or `policy_checked`.

If no workspace is specified, you have to specify a branch; the utility will search for all workspaces associated with the specified source repository and branch.


## CAVEATS
- the wait and apply is single threaded.