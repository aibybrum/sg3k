from utils import ErrorHandler


class ConfigWidgetsValidator:
    @staticmethod
    def validate_jump_df(config_widgets):
        """Validate that jump_df is not None."""
        if config_widgets.jump_df is None:
            ErrorHandler.log_and_raise_error(ValueError, "Jump data frame (jump_df) is not set.")

    @staticmethod
    def validate_config_manager(config_widgets):
        """Validate that config_manager is not None."""
        if config_widgets.config_manager is None:
            ErrorHandler.log_and_raise_error(ValueError, "Configuration manager (config_manager) is not set.")

    @staticmethod
    def validate_ready_for_visualization(config_widgets):
        """Validate that both jump_df and config_manager are not None."""
        if config_widgets.jump_df is None or config_widgets.config_manager is None:
            ErrorHandler.log_and_raise_error(
                ValueError, "Both jump_df and config_manager must be set for visualization."
            )

    @staticmethod
    def validate_config_manager_handler(config_manager_handler):
        """Validate that the configuration manager in the handler is not None."""
        if not config_manager_handler.config_manager:
            ErrorHandler.log_and_raise_error(ValueError, "Configuration manager is not set.")