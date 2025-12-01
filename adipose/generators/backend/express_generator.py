"""Express.js backend generator."""

from adipose.core.generator import CodeGenerator


class ExpressGenerator(CodeGenerator):
    """Generate Express.js backend."""
    
    def generate(self):
        """Generate Express.js backend code."""
        print("\n=== Generating Express Backend ===\n")
        
        self._generate_package_json()
        self._generate_server()
        self._generate_models()
        self._generate_routes()
        self._generate_controllers()
        self._generate_middleware()
        self._generate_utils()
        self._generate_env_example()
        
        print("\n=== Express Backend Generation Complete ===\n")
    
    def _generate_package_json(self):
        """Generate package.json."""
        context = self.get_context()
        content = self.render_template('backend/express/package.json.j2', context)
        self.write_file('package.json', content)
    
    def _generate_server(self):
        """Generate server.js main file."""
        context = self.get_context()
        content = self.render_template('backend/express/server.js.j2', context)
        self.write_file('src/server.js', content)
    
    def _generate_models(self):
        """Generate data models."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/express/model.js.j2', ctx)
            self.write_file(f'src/models/{model_name}.js', content)
    
    def _generate_routes(self):
        """Generate route definitions."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('backend/express/routes.js.j2', ctx)
            self.write_file(f'src/routes/{endpoint.resource}.js', content)
        
        # Generate main routes index
        content = self.render_template('backend/express/routes_index.js.j2', context)
        self.write_file('src/routes/index.js', content)
    
    def _generate_controllers(self):
        """Generate controllers."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('backend/express/controller.js.j2', ctx)
            self.write_file(f'src/controllers/{endpoint.resource}Controller.js', content)
    
    def _generate_middleware(self):
        """Generate middleware."""
        context = self.get_context()
        
        # Authentication middleware
        content = self.render_template('backend/express/auth_middleware.js.j2', context)
        self.write_file('src/middleware/auth.js', content)
        
        # Error handling middleware
        content = self.render_template('backend/express/error_middleware.js.j2', context)
        self.write_file('src/middleware/errorHandler.js', content)
        
        # Validation middleware
        content = self.render_template('backend/express/validation_middleware.js.j2', context)
        self.write_file('src/middleware/validation.js', content)
    
    def _generate_utils(self):
        """Generate utility files."""
        context = self.get_context()
        
        # Database connection
        content = self.render_template('backend/express/db.js.j2', context)
        self.write_file('src/config/db.js', content)
        
        # Response utilities
        content = self.render_template('backend/express/response.js.j2', context)
        self.write_file('src/utils/response.js', content)
    
    def _generate_env_example(self):
        """Generate .env.example."""
        context = self.get_context()
        content = self.render_template('backend/express/.env.example.j2', context)
        self.write_file('.env.example', content)
