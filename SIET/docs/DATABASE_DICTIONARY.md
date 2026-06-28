# Diccionario de Datos - SIET

## Tablas Principales

### users
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary Key |
| username | VARCHAR(80) | Nombre de usuario único |
| email | VARCHAR(120) | Email único |
| password_hash | VARCHAR(256) | Contraseña hasheada |
| role_id | INTEGER | Foreign Key a roles |
| first_name | VARCHAR(50) | Nombre |
| last_name | VARCHAR(50) | Apellido |
| is_active | BOOLEAN | Estado activo |
| created_at | DATETIME | Fecha creación |
| updated_at | DATETIME | Fecha actualización |

### roles
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary Key |
| name | VARCHAR(50) | Nombre del rol |
| description | VARCHAR(200) | Descripción |

### consent
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | FK a users |
| accepted | BOOLEAN | Aceptación |
| ip_address | VARCHAR(45) | IP del usuario |
| user_agent | VARCHAR(500) | User agent |
| created_at | DATETIME | Fecha aceptación |

### sessions
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | FK a users |
| start_time | DATETIME | Inicio sesión |
| end_time | DATETIME | Fin sesión |
| total_duration_seconds | INTEGER | Duración total |
| status | VARCHAR(20) | Estado |

### redtic_scores
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | FK a users |
| fatiga_tecnologica | FLOAT | Puntaje dimensión |
| ansiedad_tecnologica | FLOAT | Puntaje dimensión |
| escepticismo | FLOAT | Puntaje dimensión |
| ineficacia | FLOAT | Puntaje dimensión |
| total_score | FLOAT | Puntaje total |
| stress_level | VARCHAR(20) | Clasificación |

### stroop_results, nback_results, digitspan_results, trailmaking_results, crt_results
Tablas específicas para cada prueba cognitiva con sus respectivas métricas.

### behavior_logs
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary Key |
| session_id | INTEGER | FK a sessions |
| event_type | VARCHAR(50) | Tipo de evento |
| event_data | TEXT | Datos JSON |
| timestamp | DATETIME | Fecha evento |

### analytics_logs
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary Key |
| session_id | INTEGER | FK a sessions |
| user_id | INTEGER | FK a users |
| event_type | VARCHAR(50) | Tipo evento |
| duration_seconds | INTEGER | Duración |
| metadata | TEXT | Datos adicionales |
