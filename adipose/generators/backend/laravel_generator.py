"""Laravel backend generator."""

from adipose.core.generator import CodeGenerator


class LaravelGenerator(CodeGenerator):
    """Generate Laravel backend."""
    
    def generate(self):
        """Generate Laravel backend code."""
        print("\n=== Generating Laravel Backend ===\n")
        
        self._generate_composer_json()
        self._generate_models()
        self._generate_controllers()
        self._generate_requests()
        self._generate_resources()
        self._generate_routes()
        self._generate_middleware()
        self._generate_migrations()
        self._generate_env_example()
        
        print("\n=== Laravel Backend Generation Complete ===\n")
    
    def _generate_composer_json(self):
        """Generate composer.json."""
        context = self.get_context()
        content = self.render_template('backend/laravel/composer.json.j2', context)
        self.write_file('composer.json', content)
    
    def _generate_models(self):
        """Generate Eloquent models."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/laravel/Model.php.j2', ctx)
            self.write_file(f'app/Models/{model_name}.php', content)
    
    def _generate_controllers(self):
        """Generate API controllers."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('backend/laravel/Controller.php.j2', ctx)
            self.write_file(f'app/Http/Controllers/{endpoint.model}Controller.php', content)
    
    def _generate_requests(self):
        """Generate form request validators."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            
            # Create request
            content = self.render_template('backend/laravel/StoreRequest.php.j2', ctx)
            self.write_file(f'app/Http/Requests/Store{model_name}Request.php', content)
            
            # Update request
            content = self.render_template('backend/laravel/UpdateRequest.php.j2', ctx)
            self.write_file(f'app/Http/Requests/Update{model_name}Request.php', content)
    
    def _generate_resources(self):
        """Generate API resources."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/laravel/Resource.php.j2', ctx)
            self.write_file(f'app/Http/Resources/{model_name}Resource.php', content)
    
    def _generate_routes(self):
        """Generate API routes."""
        context = self.get_context()
        content = self.render_template('backend/laravel/api.php.j2', context)
        self.write_file('routes/api.php', content)
    
    def _generate_middleware(self):
        """Generate middleware."""
        context = self.get_context()
        
        # JWT authentication middleware
        content = self.render_template('backend/laravel/JwtMiddleware.php.j2', context)
        self.write_file('app/Http/Middleware/JwtAuthenticate.php', content)
        
        # CORS middleware
        content = self.render_template('backend/laravel/CorsMiddleware.php.j2', context)
        self.write_file('app/Http/Middleware/Cors.php', content)
    
    def _generate_migrations(self):
        """Generate database migrations."""
        context = self.get_context()
        
        for i, (model_name, model_config) in enumerate(self.config.models.items()):
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/laravel/migration.php.j2', ctx)
            
            timestamp = f"2024_01_01_{str(i).zfill(6)}"
            table_name = model_config.table_name or model_name.lower() + 's'
            self.write_file(f'database/migrations/{timestamp}_create_{table_name}_table.php', content)
    
    def _generate_env_example(self):
        """Generate .env.example."""
        context = self.get_context()
        content = self.render_template('backend/laravel/.env.example.j2', context)
        self.write_file('.env.example', content)
