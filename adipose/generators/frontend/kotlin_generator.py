"""Kotlin Android frontend generator."""

from adipose.core.generator import CodeGenerator


class KotlinGenerator(CodeGenerator):
    """Generate Kotlin Android API client."""
    
    def generate(self):
        """Generate Kotlin frontend code."""
        print("\n=== Generating Kotlin Android Frontend ===\n")
        
        self._generate_build_gradle()
        self._generate_api_client()
        self._generate_models()
        self._generate_services()
        self._generate_auth_manager()
        self._generate_error_handler()
        self._generate_interceptors()
        self._generate_config()
        
        print("\n=== Kotlin Android Frontend Generation Complete ===\n")
    
    def _generate_build_gradle(self):
        """Generate build.gradle.kts."""
        context = self.get_context()
        content = self.render_template('frontend/kotlin/build.gradle.kts.j2', context)
        self.write_file('build.gradle.kts', content)
    
    def _generate_api_client(self):
        """Generate base API client."""
        context = self.get_context()
        content = self.render_template('frontend/kotlin/ApiClient.kt.j2', context)
        self.write_file('src/main/kotlin/com/example/api/ApiClient.kt', content)
    
    def _generate_models(self):
        """Generate model classes."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('frontend/kotlin/Model.kt.j2', ctx)
            self.write_file(f'src/main/kotlin/com/example/models/{model_name}.kt', content)
    
    def _generate_services(self):
        """Generate API services."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('frontend/kotlin/Service.kt.j2', ctx)
            self.write_file(f'src/main/kotlin/com/example/services/{endpoint.model}Service.kt', content)
    
    def _generate_auth_manager(self):
        """Generate authentication manager."""
        context = self.get_context()
        content = self.render_template('frontend/kotlin/AuthManager.kt.j2', context)
        self.write_file('src/main/kotlin/com/example/auth/AuthManager.kt', content)
    
    def _generate_error_handler(self):
        """Generate error handler."""
        context = self.get_context()
        content = self.render_template('frontend/kotlin/ErrorHandler.kt.j2', context)
        self.write_file('src/main/kotlin/com/example/utils/ErrorHandler.kt', content)
    
    def _generate_interceptors(self):
        """Generate HTTP interceptors."""
        context = self.get_context()
        content = self.render_template('frontend/kotlin/Interceptors.kt.j2', context)
        self.write_file('src/main/kotlin/com/example/api/Interceptors.kt', content)
    
    def _generate_config(self):
        """Generate configuration file."""
        context = self.get_context()
        content = self.render_template('frontend/kotlin/ApiConfig.kt.j2', context)
        self.write_file('src/main/kotlin/com/example/config/ApiConfig.kt', content)
