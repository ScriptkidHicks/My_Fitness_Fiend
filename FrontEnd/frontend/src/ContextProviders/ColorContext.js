import React, { createContext, useState } from "react";

const ColorContext = createContext(undefined);
const ColorDispatchContext = createContext(undefined);

function ColorProvider({ children }) {
  const [colorTheme, setColorTheme] = useState(colorThemes.main);

  return (
    <ColorContext.Provider value={colorTheme}>
      <ColorDispatchContext.Provider value={setColorTheme}>
        {children}
      </ColorDispatchContext.Provider>
    </ColorContext.Provider>
  );
}

export { ColorContext, ColorDispatchContext, ColorProvider };

const colorThemes = {
  main: {
    primaryBackground: "#1a2f4b",
    primaryBackgroundTwo: "#122034",
    secondaryBackground: "#28475C",
    secondaryBackgroundShadow: "#08172c",
    primaryButton: "#2F8886",
    primaryButtonOutline: "#0F6866",
    primaryButtonHover: "#0F6866",
    primaryButtonHoverOutline: "#094846",
    secondaryButton: "#84C69B",
    primaryHighlights: "#A4E6BB",
    primaryText: "#FFFFFF",
    primaryError: "#D72000",
    primaryInputOutline: "#68879c",
  },
};
