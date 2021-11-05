import React, { createContext, useState } from "react";

const colorContext = createContext(undefined);
const colorDispatchContext = createContext(undefined);

function ColorProvider({ children }) {
  const [colorTheme, setColorTheme] = useState(colorThemes.main);

  return (
    <colorContext.Provider value={colorTheme}>
      <colorDispatchContext.Provider value={setColorTheme}>
        {children}
      </colorDispatchContext.Provider>
    </colorContext.Provider>
  );
}

export { colorContext, colorDispatchContext, ColorProvider };

const colorThemes = {
  main: {
    primaryBackground: "#1a2f4b",
    secondaryBackground: "#28475C",
    primaryButton: "#2F8886",
    secondaryButton: "#84C69B",
    primaryHighlights: "#A4E6BB",
    primaryText: "#FFFFFF",
    primaryError: "#D72000",
  },
};
