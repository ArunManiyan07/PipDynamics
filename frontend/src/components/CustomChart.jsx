import { useEffect, useRef } from "react";
import { createChart } from "lightweight-charts";

export default function CustomChart({ pair, timeframe }) {
  const containerRef = useRef(null);
  const chartRef = useRef(null);
  const seriesRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Create chart only once
    if (!chartRef.current) {
      const chart = createChart(containerRef.current, {
        width: containerRef.current.clientWidth,
        height: 450,
        layout: {
          background: { color: "#0b1220" },
          textColor: "#d1d5db",
        },
        grid: {
          vertLines: { color: "#1e293b" },
          horzLines: { color: "#1e293b" },
        },
      });

      const candleSeries = chart.addCandlestickSeries({
        upColor: "#2cf3ff",
        downColor: "#ff4d4f",
        borderUpColor: "#2cf3ff",
        borderDownColor: "#ff4d4f",
        wickUpColor: "#2cf3ff",
        wickDownColor: "#ff4d4f",
      });

      chartRef.current = chart;
      seriesRef.current = candleSeries;
    }

    // 🔥 Generate safe date data
    const generateData = () => {
      const data = [];
      let basePrice = 1.08;
      const startDate = new Date(2025, 0, 1);

      for (let i = 0; i < 60; i++) {
        const d = new Date(startDate);
        d.setDate(startDate.getDate() + i);

        const yyyy = d.getFullYear();
        const mm = String(d.getMonth() + 1).padStart(2, "0");
        const dd = String(d.getDate()).padStart(2, "0");

        const open = basePrice;
        const close = open + (Math.random() - 0.5) * 0.02;
        const high = Math.max(open, close) + Math.random() * 0.01;
        const low = Math.min(open, close) - Math.random() * 0.01;

        data.push({
          time: `${yyyy}-${mm}-${dd}`,
          open,
          high,
          low,
          close,
        });

        basePrice = close;
      }

      return data;
    };

    seriesRef.current.setData(generateData());
    chartRef.current.timeScale().fitContent();

    // Resize handler
    const handleResize = () => {
      chartRef.current.applyOptions({
        width: containerRef.current.clientWidth,
      });
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [pair, timeframe]);

  return (
    <div
      ref={containerRef}
      style={{ width: "100%", height: "380px" }}
    />
  );
}
