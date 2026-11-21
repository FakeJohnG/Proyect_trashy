## Reglas generales

- Una caja por objeto, ajustada al objeto (sin mucho fondo alrededor).
- Etiqueta todo objeto reconocible que se vea en la foto, aunque esté parcialmente tapado.
- Usa siempre los nombres exactos de las subclases (sin tildes ni espacios).
- Si un objeto de verdad no se puede identificar, no lo etiquetes en vez de adivinar.

## Subclases (13) y a qué clase final van

| Subclase | Clase final | Qué incluye |
|---|---|---|
| `pet` | plastico | Botellas transparentes de bebida *(sugerido; confirmar criterio)* |
| `hdpe` | plastico | Envases opacos o lechosos: leche, detergente, champú *(sugerido; confirmar)* |
| `plastico_otro` | plastico | Otros envases plásticos rígidos |
| `vidrio_botella` | vidrio | Botellas y frascos de vidrio |
| `vidrio_otro` | vidrio | Otro vidrio |
| `papel` | papel_carton | Papel, periódico, hojas |
| `carton` | papel_carton | Cajas y cartón corrugado |
| `tetrapak` | **tetrapak** | Cartones de leche y jugo. **Clase propia: va a su propio contenedor** |
| `lata_aluminio` | metal | Latas de bebida |
| `lata_acero` | metal | Latas de conserva, incluidas las de atún |
| `organico` | organico | Restos de comida y vegetales |
| `icopor` | no_reciclable | Poliestireno expandido: bandejas, vasos, relleno de empaques |
| `no_reciclable_otro` | no_reciclable | Todo lo demás, incluidas **bolsas, plástico film y envolturas** |

## Decisiones ya tomadas

- **Tetra Pak** tiene clase final propia (por eso el modelo v1 tiene 7 clases y no las 6 de la propuesta).
- **Icopor** va a `no_reciclable`.
- **Bolsas plásticas:** se eliminó la subclase. Bolsas, film y envolturas (incluidas las metalizadas de snacks) se etiquetan como `no_reciclable_otro`. Si una bolsa aparece de fondo o contiene otros objetos, no se etiqueta, pero evitar fotos donde la bolsa sea lo principal.
- **Latas de atún:** `lata_acero` (casi siempre son de acero).
- **Contenedores:** en Panamá no hay colores obligatorios; el contenedor se identifica por su rótulo. La app muestra el rótulo (`configs/destinos.json`), no un color.


## Cómo fotografiar

- Varias formas y estados del mismo material: nuevo, aplastado, sucio o roto.
- Varios colores y marcas dentro de cada clase, incluidos envases locales (así el modelo no aprende "verde = vidrio").
- Objetos que engañan: plástico transparente que parece vidrio, latas pintadas, cartón brillante, bolsas metalizadas, Tetra Pak.
- Distintas luces, ángulos, distancias y fondos reales; objetos solos y varios juntos.
- Reservar un grupo de fotos que **nunca** se use para entrenar, idealmente tomadas por otra persona o en otro lugar.
- Cuidado con muchas fotos casi idénticas del mismo objeto: inflan las métricas.

## Licencias de datos externos

Si mezclamos datasets públicos (TACO, TrashNet, Roboflow Universe), anotar aquí la licencia de cada uno:

| Dataset | Licencia | Notas |
|---|---|---|
| | | |
