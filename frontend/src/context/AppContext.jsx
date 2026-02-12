import React, { createContext, useState } from "react";

export const AppContext = createContext();

export function AppProvider({ children }) {
  const [pair, setPair] = useState("EUR/USD");
  const [timeframe, setTimeframe] = useState("M15");

  return (
    <AppContext.Provider
      value={{ pair, setPair, timeframe, setTimeframe }}
    >
      {children}
    </AppContext.Provider>
  );
}
