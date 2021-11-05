import React, { createContext, useState } from "react";

const ColorContext = createContext(undefined);
const ColorDispatchContext = createContext(undefined);

function ColorProvider({ children }) {
  const [colorTheme, setColorTheme] = useState(colorThemes.main);
  console.log("from inside", colorTheme);

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
    primaryBackgroundTwo: "##122034",
    secondaryBackground: "#28475C",
    primaryButton: "#2F8886",
    secondaryButton: "#84C69B",
    primaryHighlights: "#A4E6BB",
    primaryText: "#FFFFFF",
    primaryError: "#D72000",
  },
};
