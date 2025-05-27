# Archivos de inicio automático para el sistema

Este directorio contiene los scripts y servicios necesarios para que el servidor y la notificación de IP se ejecuten automáticamente al iniciar el sistema.

---

## 📁 Estructura de archivos

### Scripts a copiar en `/opt/mi_proyecto/`
- `envar_ip.py`: Script que envía la IP pública por Telegram al iniciar.
- `iniciar_servidor.py`: Script que arranca Django, ngrok, Celery, etc.

### Servicios a copiar en `/etc/systemd/system/`
- `enviar-ip.service`: Servicio systemd que lanza `envar_ip.py` al arranque.
- `mi_servidor.service`: Servicio systemd que lanza `iniciar_servidor.py`.

---

## 🛠 Instrucciones de instalación

1. Crea la carpeta de destino si no existe:
   ```bash
   sudo mkdir -p /opt/mi_proyecto
````

2. Copia los scripts a `/opt/mi_proyecto/`:

   ```bash
   sudo cp envar_ip.py iniciar_servidor.py /opt/mi_proyecto/
   ```

3. Copia los servicios a `/etc/systemd/system/`:

   ```bash
   sudo cp enviar-ip.service mi_servidor.service /etc/systemd/system/
   ```

4. Da permisos de ejecución a los scripts:

   ```bash
   sudo chmod +x /opt/mi_proyecto/envar_ip.py
   sudo chmod +x /opt/mi_proyecto/iniciar_servidor.py
   ```

5. Recarga y habilita los servicios:

   ```bash
   sudo systemctl daemon-reexec
   sudo systemctl daemon-reload
   sudo systemctl enable enviar-ip.service
   sudo systemctl enable mi_servidor.service
   sudo systemctl start enviar-ip.service
   sudo systemctl start mi_servidor.service
   ```

6. Verifica que estén activos:

   ```bash
   systemctl status enviar-ip.service
   systemctl status mi_servidor.service
   ```

---

## 🔁 Notas

* Asegúrate de tener configurado correctamente `envar_ip.py` con tu token y chat ID de Telegram.
* Puedes editar los archivos `.service` para ajustar el usuario o ruta si cambian.

---

## 📦 Autor y mantenimiento

Este sistema está diseñado para automatizar el arranque de servicios esenciales del proyecto `inventario-elconet` en un entorno headless (como Raspberry Pi o servidor Ubuntu).

