"""ASP.NET Core backend generator."""

from adipose.core.generator import CodeGenerator


class DotNetGenerator(CodeGenerator):
    """Generate ASP.NET Core backend."""
    
    def generate(self):
        """Generate .NET backend code."""
        print("\n=== Generating .NET Backend ===\n")
        
        self._generate_csproj()
        self._generate_program()
        self._generate_models()
        self._generate_dtos()
        self._generate_controllers()
        self._generate_services()
        self._generate_dbcontext()
        self._generate_middleware()
        self._generate_appsettings()
        
        print("\n=== .NET Backend Generation Complete ===\n")
    
    def _generate_csproj(self):
        """Generate .csproj file."""
        context = self.get_context()
        content = self.render_template('backend/dotnet/project.csproj.j2', context)
        self.write_file(f'{self.config.project.name}.csproj', content)
    
    def _generate_program(self):
        """Generate Program.cs."""
        context = self.get_context()
        content = self.render_template('backend/dotnet/Program.cs.j2', context)
        self.write_file('Program.cs', content)
    
    def _generate_models(self):
        """Generate entity models."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/dotnet/Model.cs.j2', ctx)
            self.write_file(f'Models/{model_name}.cs', content)
    
    def _generate_dtos(self):
        """Generate DTOs."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/dotnet/Dto.cs.j2', ctx)
            self.write_file(f'DTOs/{model_name}Dto.cs', content)
    
    def _generate_controllers(self):
        """Generate API controllers."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('backend/dotnet/Controller.cs.j2', ctx)
            self.write_file(f'Controllers/{endpoint.model}Controller.cs', content)
    
    def _generate_services(self):
        """Generate service layer."""
        context = self.get_context()
        for model_name in self.config.models.keys():
            ctx = {**context, 'model_name': model_name}
            content = self.render_template('backend/dotnet/Service.cs.j2', ctx)
            self.write_file(f'Services/{model_name}Service.cs', content)
    
    def _generate_dbcontext(self):
        """Generate DbContext."""
        context = self.get_context()
        content = self.render_template('backend/dotnet/DbContext.cs.j2', context)
        self.write_file('Data/ApplicationDbContext.cs', content)
    
    def _generate_middleware(self):
        """Generate middleware."""
        context = self.get_context()
        
        # JWT authentication middleware
        content = self.render_template('backend/dotnet/AuthMiddleware.cs.j2', context)
        self.write_file('Middleware/AuthenticationMiddleware.cs', content)
        
        # Error handling middleware
        content = self.render_template('backend/dotnet/ErrorMiddleware.cs.j2', context)
        self.write_file('Middleware/ErrorHandlingMiddleware.cs', content)
    
    def _generate_appsettings(self):
        """Generate appsettings.json."""
        context = self.get_context()
        content = self.render_template('backend/dotnet/appsettings.json.j2', context)
        self.write_file('appsettings.json', content)
