#!/usr/bin/env bats
# Sources check-env.sh (guarded by the BASH_SOURCE check at its bottom, so
# sourcing it here doesn't run main) and tests its functions directly —
# isolated from stdout formatting and the script's own exit-code wrapper.

setup() {
    load "${BATS_TEST_DIRNAME}/../scripts/check-env.sh"
}

@test "command_exists returns success for a real command" {
    run command_exists bash
    [ "$status" -eq 0 ]
}

@test "command_exists returns failure for a made-up command" {
    run command_exists totally-not-a-real-tool
    [ "$status" -ne 0 ]
}

@test "check_tool reports OK for an installed tool" {
    run check_tool bash
    [ "$status" -eq 0 ]
    [[ "$output" == OK* ]]
}

@test "check_tool reports MISSING for a missing tool" {
    run check_tool totally-not-a-real-tool
    [ "$status" -ne 0 ]
    [[ "$output" == MISSING* ]]
}
