def get_step_output() -> dict:
    """
    Returns the output returned by the current step.

    For Lambda flows, this method can be used in `after_escalate` and `after_deescalate` hooks
    to retrieve responses from the lambda.

    For example::

        @hook
        def after_escalate(evt):
            escalate_output = get_step_output()
            print(escalate_output["body"])
    """
