"""Spring Boot backend generator."""

from adipose.core.generator import CodeGenerator


class SpringBootGenerator(CodeGenerator):
    """Generate Spring Boot backend."""
    
    def generate(self):
        """Generate Spring Boot backend code."""
        print("\n=== Generating Spring Boot Backend ===\n")
        
        self._generate_pom()
        self._generate_application()
        self._generate_entities()
        self._generate_repositories()
        self._generate_services()
        self._generate_controllers()
        self._generate_dtos()
        self._generate_security()
        self._generate_application_properties()
        
        print("\n=== Spring Boot Backend Generation Complete ===\n")
    
    def _generate_pom(self):
        """Generate pom.xml."""
        context = self.get_context()
        content = self.render_template('backend/springboot/pom.xml.j2', context)
        self.write_file('pom.xml', content)
    
    def _generate_application(self):
        """Generate main application class."""
        context = self.get_context()
        content = self.render_template('backend/springboot/Application.java.j2', context)
        package_path = 'src/main/java/com/example/' + self.config.project.name.lower()
        self.write_file(f'{package_path}/Application.java', content)
    
    def _generate_entities(self):
        """Generate JPA entities."""
        context = self.get_context()
        package_path = 'src/main/java/com/example/' + self.config.project.name.lower()
        
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/springboot/Entity.java.j2', ctx)
            self.write_file(f'{package_path}/entity/{model_name}.java', content)
    
    def _generate_repositories(self):
        """Generate JPA repositories."""
        context = self.get_context()
        package_path = 'src/main/java/com/example/' + self.config.project.name.lower()
        
        for model_name in self.config.models.keys():
            ctx = {**context, 'model_name': model_name}
            content = self.render_template('backend/springboot/Repository.java.j2', ctx)
            self.write_file(f'{package_path}/repository/{model_name}Repository.java', content)
    
    def _generate_services(self):
        """Generate service layer."""
        context = self.get_context()
        package_path = 'src/main/java/com/example/' + self.config.project.name.lower()
        
        for model_name in self.config.models.keys():
            ctx = {**context, 'model_name': model_name}
            content = self.render_template('backend/springboot/Service.java.j2', ctx)
            self.write_file(f'{package_path}/service/{model_name}Service.java', content)
    
    def _generate_controllers(self):
        """Generate REST controllers."""
        context = self.get_context()
        package_path = 'src/main/java/com/example/' + self.config.project.name.lower()
        
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('backend/springboot/Controller.java.j2', ctx)
            self.write_file(f'{package_path}/controller/{endpoint.model}Controller.java', content)
    
    def _generate_dtos(self):
        """Generate DTOs."""
        context = self.get_context()
        package_path = 'src/main/java/com/example/' + self.config.project.name.lower()
        
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('backend/springboot/Dto.java.j2', ctx)
            self.write_file(f'{package_path}/dto/{model_name}Dto.java', content)
    
    def _generate_security(self):
        """Generate security configuration."""
        context = self.get_context()
        package_path = 'src/main/java/com/example/' + self.config.project.name.lower()
        
        content = self.render_template('backend/springboot/SecurityConfig.java.j2', context)
        self.write_file(f'{package_path}/config/SecurityConfig.java', content)
        
        content = self.render_template('backend/springboot/JwtFilter.java.j2', context)
        self.write_file(f'{package_path}/security/JwtFilter.java', content)
    
    def _generate_application_properties(self):
        """Generate application.properties."""
        context = self.get_context()
        content = self.render_template('backend/springboot/application.properties.j2', context)
        self.write_file('src/main/resources/application.properties', content)
