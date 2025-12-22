# Configuración de DeepSeek API

## ¿Qué es DeepSeek?

DeepSeek es un modelo de IA avanzado que reemplaza a Gemini en este bot. Ventajas:

- ✅ **Muy económico**: ~$0.14 por 1M tokens de entrada, $0.28 por 1M tokens de salida
- ✅ **Sin límites de cuota estrictos**: No tendrás errores de "quota exceeded"
- ✅ **Responde perfectamente en español**: Multilingüe nativo
- ✅ **Soporta visión**: Puede analizar imágenes
- ✅ **Compatible con OpenAI API**: Fácil de usar

## Cómo obtener tu API Key

1. Ve a [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. Crea una cuenta (puedes usar Google/GitHub)
3. Ve a "API Keys" en el menú
4. Haz clic en "Create API Key"
5. Copia la clave (empieza con `sk-...`)

## Configuración en el Bot

### Opción 1: Variables de entorno (Recomendado para Docker)

Agrega esta línea a tu archivo `.env`:

```env
DEEPSEEK_API_KEY=sk-tu-clave-aqui
```

### Opción 2: Variable de sistema (Para desarrollo local)

**Windows PowerShell:**
```powershell
$env:DEEPSEEK_API_KEY="sk-tu-clave-aqui"
```

**Linux/Mac:**
```bash
export DEEPSEEK_API_KEY="sk-tu-clave-aqui"
```

## Uso en Discord

Los comandos siguen siendo los mismos:

```
>gemini hola, ¿cómo estás?
>gemini --lang en what's the weather like?
>gemini_reset
>gemini_help
```

## Costos aproximados

Con $5 USD de crédito puedes procesar aproximadamente:
- **35 millones de tokens de entrada** (~26,000 páginas de texto)
- **17 millones de tokens de salida** (~13,000 páginas de respuestas)

Para un bot de Discord personal, $5 puede durar **meses**.

## Solución de problemas

**Error: "DEEPSEEK_API_KEY no está configurada"**
- Verifica que agregaste la clave al archivo `.env`
- Si usas Docker, reconstruye la imagen: `docker compose build bot`
- Si es local, verifica que la variable de entorno esté configurada

**El bot no responde:**
- Verifica que la API key sea válida
- Revisa los logs: `docker compose logs bot`
- Asegúrate de tener créditos en tu cuenta DeepSeek
