-- Evaluación 3: los usuarios inician sesión con una contraseña
-- Se guarda el hash de Bcrypt (60 caracteres), nunca la contraseña en texto plano
ALTER TABLE usuarios ADD COLUMN contrasena VARCHAR(60) NULL;
