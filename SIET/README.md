# SIET - Sistema Inteligente de Evaluación de Tecnoestrés

## Descripción

SIET es un prototipo de investigación científica diseñado para evaluar el tecnoestrés mediante un enfoque híbrido que integra:

- **Cuestionario RED-TIC**: Instrumento psicométrico validado
- **Pruebas Cognitivas Digitales**: Stroop, N-Back, Digit Span, Trail Making, CRT
- **Learning Analytics**: Captura automática de métricas de aprendizaje
- **Behavioral Analytics**: Registro de interacciones del usuario
- **Dashboards Interactivos**: Visualización de resultados con Chart.js

## Requisitos Técnicos

- Python 3.12+
- Flask 3.0+
- SQLite
- Navegador moderno (Chrome, Firefox, Edge)

## Instalación

```bash
cd SIET
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## Credenciales por Defecto

- **Usuario**: admin
- **Contraseña**: admin123
- **Email**: admin@siet.local

## Estructura del Proyecto

```
SIET/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── routes/          # Rutas y controladores
│   ├── analytics/       # Motor analítico
│   ├── psychometrics/   # Cuestionarios psicométricos
│   ├── services/        # Servicios de negocio
│   └── forms/           # Formularios WTForms
├── templates/           # Plantillas HTML
├── static/
│   ├── css/            # Hojas de estilo
│   └── js/             # JavaScript (pruebas cognitivas)
├── database/           # Base de datos SQLite
├── config.py           # Configuración
└── run.py              # Punto de entrada
```

## Características

### Usuarios y Roles
- **Administrador**: Gestión completa del sistema
- **Investigador**: Acceso a dashboards y exportación de datos
- **Estudiante**: Realiza evaluaciones y consulta resultados

### Evaluación RED-TIC
- 20 preguntas con escala Likert 1-5
- 4 dimensiones: Fatiga, Ansiedad, Escepticismo, Ineficacia
- Clasificación automática del nivel de tecnoestrés

### Pruebas Cognitivas
1. **Stroop Test**: 20 ensayos, mide interferencia cognitiva
2. **N-Back (2-Back)**: 20 estímulos, evalúa memoria de trabajo
3. **Digit Span**: Forward y Backward, mide capacidad de memoria
4. **Trail Making Test**: Versiones A y B, flexibilidad cognitiva
5. **Cognitive Reflection Test**: 3 preguntas clásicas

### Analytics
- Tiempo total de sesión
- Tiempo por pregunta/prueba
- Cambios de respuesta
- Eventos de comportamiento (scroll, focus, blur)

## Consideraciones de Investigación

**IMPORTANTE**: Este es un prototipo de investigación:
- NO implementa modelos predictivos entrenados
- NO utiliza datasets reales
- NO implementa Machine Learning
- La IA es una arquitectura preparada para futuras investigaciones
- Los resultados NO constituyen diagnóstico médico

## Licencia

Proyecto académico de investigación.

## Autores

Desarrollado como prototipo para investigación científica en tecnoestrés.
