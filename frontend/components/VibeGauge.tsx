"use client";

import React from "react";

interface VibeGaugeProps {
  score: number;
  size?: number;
  strokeWidth?: number;
}

export function VibeGauge({ score, size = 160, strokeWidth = 14 }: VibeGaugeProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.min(100, Math.max(0, score));
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  let color = "#10B981"; // Emerald Green
  let statusText = "Vibe Certified 🛡️";
  let badgeBg = "bg-safe/10 text-safe border-safe/30";

  if (score < 50) {
    color = "#EF4444"; // Crimson Red
    statusText = "Danger Zone 🚨";
    badgeBg = "bg-critical/10 text-critical border-critical/30";
  } else if (score < 70) {
    color = "#F59E0B"; // Amber Orange
    statusText = "Needs Attention ⚠️";
    badgeBg = "bg-warning/10 text-warning border-warning/30";
  } else if (score < 90) {
    color = "#8B5CF6"; // Electric Violet
    statusText = "Looking Great 👍";
    badgeBg = "bg-brand/10 text-brand border-brand/30";
  }

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background Track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#21262D"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Animated Health Ring */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center Score Readout */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-3xl sm:text-4xl font-extrabold text-cyber-bright tracking-tight font-mono">
            {score}
          </span>
          <span className="text-[10px] text-cyber-muted uppercase tracking-wider font-semibold">
            Health Score
          </span>
        </div>
      </div>

      <div className={`mt-3 inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${badgeBg}`}>
        {statusText}
      </div>
    </div>
  );
}
