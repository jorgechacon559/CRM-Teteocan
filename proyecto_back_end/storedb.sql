-- Crear base de datos y usar esquema
CREATE DATABASE IF NOT EXISTS storedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE storedb;

-- Tabla para control de migraciones de Alembic
CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de usuarios (roles: admin, agente)
CREATE TABLE IF NOT EXISTS `usuarios` (
  `usuario_id` int NOT NULL AUTO_INCREMENT,
  `rol` ENUM('admin', 'agente') NOT NULL DEFAULT 'agente',
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `baja` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla principal de organizaciones
CREATE TABLE IF NOT EXISTS `organizaciones` (
  `organizacion_id` int NOT NULL AUTO_INCREMENT,
  `tipo` ENUM('empresa', 'negocio_local') NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email_contacto` varchar(100) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `ubicacion` varchar(150) DEFAULT NULL, 
  `sector` varchar(100) DEFAULT NULL,    
  `categoria` varchar(100) DEFAULT NULL,
  `sitio_web` varchar(255) DEFAULT NULL,
  `notas` text,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `prospecto_id` int DEFAULT NULL COMMENT 'Agente asignado',
  `nivel_digitalizacion` TINYINT NOT NULL DEFAULT 0 COMMENT '0: Sin info, 1: Nada, 2: Solo RS/WA, 3: Solo Web, 4: Combinación, 5: Completo',
  `estado_organizacion` ENUM('prospecto', 'cliente', 'descartado') NOT NULL DEFAULT 'prospecto',
  PRIMARY KEY (`organizacion_id`),
  KEY `fk_prospecto` (`prospecto_id`),
  CONSTRAINT `fk_prospecto` FOREIGN KEY (`prospecto_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de detalles específicos para empresas
CREATE TABLE IF NOT EXISTS `detalles_empresas` (
  `empresa_id` int NOT NULL AUTO_INCREMENT,
  `organizacion_id` int NOT NULL,
  `numero_empleados` int DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`empresa_id`),
  KEY `fk_empresa_org` (`organizacion_id`),
  CONSTRAINT `fk_empresa_org` FOREIGN KEY (`organizacion_id`) REFERENCES `organizaciones` (`organizacion_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de detalles específicos para negocios locales
CREATE TABLE IF NOT EXISTS `detalles_negocios` (
  `negocio_id` int NOT NULL AUTO_INCREMENT,
  `organizacion_id` int NOT NULL,
  `horario_apertura` time DEFAULT NULL,
  `horario_cierre` time DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`negocio_id`),
  KEY `fk_negocio_org` (`organizacion_id`),
  CONSTRAINT `fk_negocio_org` FOREIGN KEY (`organizacion_id`) REFERENCES `organizaciones` (`organizacion_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de seguimientos
CREATE TABLE IF NOT EXISTS `seguimientos` (
  `seguimiento_id` int NOT NULL AUTO_INCREMENT,
  `organizacion_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo` ENUM('prospeccion', 'seguimiento', 'cierre') NOT NULL,
  `nivel_digitalizacion` TINYINT DEFAULT NULL COMMENT '0: Sin info, 1: Nada, 2: Solo RS/WA, 3: Solo Web, 4: Combinación, 5: Completo',
  `estado` ENUM('prospecto', 'contactado', 'no_responde', 'interesado', 'cliente', 'descartado') DEFAULT NULL,
  `comentarios` text,
  `metodo_contacto` ENUM('whatsapp', 'email', 'llamada', 'visita', 'otro') DEFAULT NULL,
  `fecha_actualizacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`seguimiento_id`),
  KEY `fk_seguimiento_org` (`organizacion_id`),
  KEY `fk_seguimiento_usuario` (`usuario_id`),
  CONSTRAINT `fk_seguimiento_org` FOREIGN KEY (`organizacion_id`) REFERENCES `organizaciones` (`organizacion_id`),
  CONSTRAINT `fk_seguimiento_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de historial de asignaciones (para auditoría)
CREATE TABLE IF NOT EXISTS `asignaciones_prospectos` (
  `asignacion_id` int NOT NULL AUTO_INCREMENT,
  `organizacion_id` int NOT NULL,
  `usuario_id` int NOT NULL COMMENT 'Agente asignado',
  `fecha_asignacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_finalizacion` datetime DEFAULT NULL,
  `fecha_actualizacion` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`asignacion_id`),
  KEY `fk_asignacion_org` (`organizacion_id`),
  KEY `fk_asignacion_usuario` (`usuario_id`),
  CONSTRAINT `fk_asignacion_org` FOREIGN KEY (`organizacion_id`) REFERENCES `organizaciones` (`organizacion_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_asignacion_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TRIGGER 1: Asignación automática al primer seguimiento
DELIMITER //
CREATE TRIGGER asignar_prospecto
AFTER INSERT ON seguimientos
FOR EACH ROW
BEGIN
  DECLARE current_prospecto INT;
  
  SELECT prospecto_id INTO current_prospecto 
  FROM organizaciones 
  WHERE organizacion_id = NEW.organizacion_id;
  
  -- Si no hay prospecto asignado, asignar al usuario del seguimiento
  IF current_prospecto IS NULL THEN
    UPDATE organizaciones 
    SET prospecto_id = NEW.usuario_id
    WHERE organizacion_id = NEW.organizacion_id;
  END IF;
  
  -- Actualizar estado si se proporciona
  IF NEW.estado IS NOT NULL THEN
    UPDATE organizaciones 
    SET estado_organizacion = NEW.estado
    WHERE organizacion_id = NEW.organizacion_id;
  END IF;
  
  -- Actualizar nivel de digitalización si se proporciona
  IF NEW.nivel_digitalizacion IS NOT NULL THEN
    UPDATE organizaciones 
    SET nivel_digitalizacion = NEW.nivel_digitalizacion
    WHERE organizacion_id = NEW.organizacion_id;
  END IF;
END;
//
DELIMITER ;

-- TRIGGER 2: Registrar asignación cuando se actualiza prospecto_id
DELIMITER //
CREATE TRIGGER registrar_asignacion
AFTER UPDATE ON organizaciones
FOR EACH ROW
BEGIN
  -- Si cambió la asignación
  IF OLD.prospecto_id <> NEW.prospecto_id OR (OLD.prospecto_id IS NULL AND NEW.prospecto_id IS NOT NULL) THEN
    -- Cerrar asignación anterior si existe
    IF OLD.prospecto_id IS NOT NULL THEN
      UPDATE asignaciones_prospectos 
      SET fecha_finalizacion = NOW()
      WHERE organizacion_id = NEW.organizacion_id
        AND usuario_id = OLD.prospecto_id
        AND fecha_finalizacion IS NULL;
    END IF;
    
    -- Crear nueva asignación
    IF NEW.prospecto_id IS NOT NULL THEN
      INSERT INTO asignaciones_prospectos (organizacion_id, usuario_id)
      VALUES (NEW.organizacion_id, NEW.prospecto_id);
    END IF;
  END IF;
END;
//
DELIMITER ;
