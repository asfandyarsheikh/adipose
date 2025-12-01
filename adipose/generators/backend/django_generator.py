"""Django backend generator."""

from adipose.core.generator import CodeGenerator


class DjangoGenerator(CodeGenerator):
    """Generate Django REST Framework backend."""
    
    def generate(self):
        """Generate Django backend code."""
        print("\n=== Generating Django Backend ===\n")
        
        # Generate project structure
        self._generate_settings()
        self._generate_urls()
        self._generate_models()
        self._generate_serializers()
        self._generate_views()
        self._generate_authentication()
        self._generate_middleware()
        self._generate_requirements()
        self._generate_manage_py()
        
        print("\n=== Django Backend Generation Complete ===\n")
    
    def _generate_settings(self):
        """Generate Django settings file."""
        context = self.get_context()
        content = self.render_template('backend/django/settings.py.j2', context)
        self.write_file(f'{self.config.project.name}/settings.py', content)
    
    def _generate_urls(self):
        """Generate URL configuration."""
        context = self.get_context()
        content = self.render_template('backend/django/urls.py.j2', context)
        self.write_file(f'{self.config.project.name}/urls.py', content)
    
    def _generate_models(self):
        """Generate Django models."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/django/model.py.j2', ctx)
            self.write_file(f'api/models/{model_name.lower()}.py', content)
        
        # Generate __init__.py for models
        model_imports = '\n'.join([
            f"from .{name.lower()} import {name}" 
            for name in self.config.models.keys()
        ])
        self.write_file('api/models/__init__.py', model_imports)
    
    def _generate_serializers(self):
        """Generate DRF serializers."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/django/serializer.py.j2', ctx)
            self.write_file(f'api/serializers/{model_name.lower()}.py', content)
    
    def _generate_views(self):
        """Generate Django views."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('backend/django/viewset.py.j2', ctx)
            self.write_file(f'api/views/{endpoint.resource}.py', content)
    
    def _generate_authentication(self):
        """Generate authentication middleware."""
        context = self.get_context()
        content = self.render_template('backend/django/authentication.py.j2', context)
        self.write_file('api/authentication.py', content)
    
    def _generate_middleware(self):
        """Generate custom middleware."""
        context = self.get_context()
        content = self.render_template('backend/django/middleware.py.j2', context)
        self.write_file('api/middleware.py', content)
    
    def _generate_requirements(self):
        """Generate requirements.txt."""
        requirements = [
            'Django>=4.2.0',
            'djangorestframework>=3.14.0',
            'django-cors-headers>=4.0.0',
            'PyJWT>=2.8.0',
            'python-dotenv>=1.0.0',
        ]
        
        if self.config.database.type == 'postgresql':
            requirements.append('psycopg2-binary>=2.9.0')
        elif self.config.database.type == 'mysql':
            requirements.append('mysqlclient>=2.2.0')
        
        self.write_file('requirements.txt', '\n'.join(requirements))
    
    def _generate_manage_py(self):
        """Generate manage.py."""
        context = self.get_context()
        content = self.render_template('backend/django/manage.py.j2', context)
        self.write_file('manage.py', content)
