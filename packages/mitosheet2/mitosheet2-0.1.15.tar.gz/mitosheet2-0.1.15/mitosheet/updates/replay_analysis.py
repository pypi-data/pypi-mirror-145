#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.
"""
Replays an existing analysis onto the sheet
"""

from typing import Any, Dict
from mitosheet.errors import make_no_analysis_error

from mitosheet.mito_analytics import log
from mitosheet.saved_analyses import read_and_upgrade_analysis
from mitosheet.types import StepsManagerType

REPLAY_ANALYSIS_UPDATE_EVENT = 'replay_analysis_update'
REPLAY_ANALYSIS_UPDATE_PARAMS = [
    'analysis_name',
    'import_summaries',
    'clear_existing_analysis',
]

def execute_replay_analysis_update(
        steps_manager: StepsManagerType,
        analysis_name: str,
        import_summaries: Dict[str, Any],
        clear_existing_analysis: bool
    ) -> None:
    """
    This function reapplies all the steps summarized in the passed step summaries, 
    which come from a saved analysis. 

    If any of the step summaries fails, this function tries to roll back to before
    it applied any of the stems

    If clear_existing_analysis is set to true, then this will clear the entire widget
    state container (except the initalize step) before applying the saved analysis.
    """

    # If we're getting an event telling us to update, we read in the steps from the file
    analysis = read_and_upgrade_analysis(analysis_name)

    # If there is no analysis with this name, generate an error. This must occur before  
    # steps_manager.steps = steps_manager.steps[:1] so that we don't clear all of the user's generated code. 
    # This is particularly important for users who received the notebook from a colleague.
    if analysis is None:
        log('replayed_nonexistant_analysis_failed')
        raise make_no_analysis_error(analysis_name)


    # We only keep the intialize step only, if we want to clear,
    # and also update the analysis name to the replayed analysis
    # NOTE: we update the analysis name so that when the code
    # is written on the front-end, this analysis is correctly
    # overwritten entirely (as this analysis being replayed entirely
    # means that it is effectively being replaced)
    if clear_existing_analysis:
        steps_manager.steps = steps_manager.steps[:1]
        steps_manager.analysis_name = analysis_name

    # When replaying an analysis with import events, you can also send over
    # new params to the import events to replace them. We replace them in the steps here
    if import_summaries is not None:
        for step_idx, file_names in import_summaries.items():
            # NOTE: we have to parse the step index, as it is a string (as it is
            # sent in JSON, which only has strings as keys
            analysis['steps_data'][int(step_idx)]['params']['file_names'] = file_names

    # We stupidly store our saved steps here as a mapping, so we go through and turn it into 
    # a list so that we can pass it into other functions
    # If the analysis is getting replayed because of replaying a saved analysis through the Mitosheet UI, 
    # then we filter out the set_cell_value steps 
    if not clear_existing_analysis:
        steps_excluding_set_cell_value_steps = list(filter(skip_set_cell_value_steps, analysis['steps_data']))
    else: 
        steps_excluding_set_cell_value_steps = analysis['steps_data']
    steps_manager.execute_steps_data(new_steps_data=steps_excluding_set_cell_value_steps)

def skip_set_cell_value_steps(step_data):
    """
    Helper function for filtering out set_cell_value steps. We do this when
    the analysis is getting replayed because of replaying a saved analysis.
    """
    if step_data['step_type'] == 'set_cell_value':
        return False
    return True

REPLAY_ANALYSIS_UPDATE = {
    'event_type': REPLAY_ANALYSIS_UPDATE_EVENT,
    'params': REPLAY_ANALYSIS_UPDATE_PARAMS,
    'execute': execute_replay_analysis_update
}
