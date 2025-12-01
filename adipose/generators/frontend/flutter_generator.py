"""Flutter/Dart frontend generator."""

from adipose.core.generator import CodeGenerator


class FlutterGenerator(CodeGenerator):
    """Generate Flutter/Dart API client."""
    
    def generate(self):
        """Generate Flutter frontend code."""
        print("\n=== Generating Flutter Frontend ===\n")
        
        self._generate_pubspec()
        self._generate_api_client()
        self._generate_models()
        self._generate_services()
        self._generate_auth_manager()
        self._generate_error_handler()
        self._generate_interceptors()
        self._generate_config()
        
        print("\n=== Flutter Frontend Generation Complete ===\n")
    
    def _generate_pubspec(self):
        """Generate pubspec.yaml."""
        context = self.get_context()
        content = self.render_template('frontend/flutter/pubspec.yaml.j2', context)
        self.write_file('pubspec.yaml', content)
    
    def _generate_api_client(self):
        """Generate base API client."""
        context = self.get_context()
        content = self.render_template('frontend/flutter/api_client.dart.j2', context)
        self.write_file('lib/api/api_client.dart', content)
    
    def _generate_models(self):
        """Generate model classes."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('frontend/flutter/model.dart.j2', ctx)
            self.write_file(f'lib/models/{model_name.lower()}.dart', content)
    
    def _generate_services(self):
        """Generate API services."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('frontend/flutter/service.dart.j2', ctx)
            self.write_file(f'lib/services/{endpoint.resource}_service.dart', content)
    
    def _generate_auth_manager(self):
        """Generate authentication manager."""
        context = self.get_context()
        content = self.render_template('frontend/flutter/auth_manager.dart.j2', context)
        self.write_file('lib/auth/auth_manager.dart', content)
    
    def _generate_error_handler(self):
        """Generate error handler."""
        context = self.get_context()
        content = self.render_template('frontend/flutter/error_handler.dart.j2', context)
        self.write_file('lib/utils/error_handler.dart', content)
    
    def _generate_interceptors(self):
        """Generate HTTP interceptors."""
        context = self.get_context()
        content = self.render_template('frontend/flutter/interceptors.dart.j2', context)
        self.write_file('lib/api/interceptors.dart', content)
    
    def _generate_config(self):
        """Generate configuration file."""
        context = self.get_context()
        content = self.render_template('frontend/flutter/api_config.dart.j2', context)
        self.write_file('lib/config/api_config.dart', content)
