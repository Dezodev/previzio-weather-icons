/**
 * previzio-weather-icons — helper léger pour résoudre une icône à partir d'un code WMO.
 *
 * Usage :
 *   import { iconPath, ICON_INDEX } from "./wmo-icons.js";
 *   const url = iconPath(61, "day"); // -> "icons/61-day.svg"
 */
import index from "./index.json" assert { type: "json" };

export const ICON_INDEX = index.icons;

/**
 * Retourne le chemin du fichier SVG pour un code WMO donné.
 * @param {number|string} code  Code WMO (0, 1, 2, 3, 45, 48, 51...).
 * @param {"day"|"night"} [variant="day"]  Variante voulue.
 * @returns {string|null}  Chemin relatif vers le SVG, ou null si inconnu.
 */
export function iconPath(code, variant = "day") {
  const entry = ICON_INDEX[String(code)];
  if (!entry) return null;
  const file = variant === "night" ? entry.night : entry.day;
  return `icons/${file}`;
}

/**
 * Choisit automatiquement jour/nuit selon une heure ou un flag isDay.
 * @param {number|string} code
 * @param {boolean} isDay
 */
export function iconPathAuto(code, isDay) {
  return iconPath(code, isDay ? "day" : "night");
}
