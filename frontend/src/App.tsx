import React, { useState } from 'react';

interface Player {
  id: number;
  name: string;
  x: number;
  y: number;
  team: 'def' | 'att';
}

const TacticalOS: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [defensiveBlock, setDefensiveBlock] = useState<'low' | 'mid' | 'high'>('mid');
  const [horizontalShift, setHorizontalShift] = useState(68);
  const [verticalCompactness, setVerticalCompactness] = useState(42);
  const [showVoronoi, setShowVoronoi] = useState(true);
  const [showVisionCones, setShowVisionCones] = useState(false);
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [showSpaceAnalysis, setShowSpaceAnalysis] = useState(false);
  const [timelineProgress, setTimelineProgress] = useState(45);
  const [currentTime, setCurrentTime] = useState('00:14');

  const players: Player[] = [
    { id: 1, name: '4', x: 20, y: 30, team: 'def' },
    { id: 2, name: '3', x: 20, y: 70, team: 'def' },
    { id: 3, name: '5', x: 30, y: 50, team: 'def' },
    { id: 4, name: '8', x: 45, y: 40, team: 'def' },
    { id: 5, name: '9', x: 50, y: 70, team: 'att' },
    { id: 6, name: '10', x: 65, y: 55, team: 'att' },
    { id: 7, name: '7', x: 70, y: 30, team: 'att' },
  ];

  const handleTimelineClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = (x / rect.width) * 100;
    setTimelineProgress(percentage);
  };

  return (
    <div className="flex flex-col h-screen antialiased text-[var(--color-text-primary)] selection:bg-[var(--color-primary-container)] selection:text-[var(--color-on-primary-container)]">
      {/* ===== TopNavBar ===== */}
      <header className="fixed top-0 w-full z-50 flex justify-between items-center px-[24px] h-16 bg-[#111827b8] backdrop-blur-xl border-b border-[#ffffff14]">
        <div className="flex items-center gap-[8px]">
          <span
            className="material-symbols-outlined text-[var(--color-primary)] text-[28px]"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            speed
          </span>
          <span className="font-headline-lg font-bold text-[var(--color-primary)] tracking-tight">TacticalOS</span>
          <span className="ml-4 font-stats-md text-[var(--color-tertiary)] flex items-center gap-2 px-3 py-1 bg-[var(--color-tertiary-container)]/10 rounded-full border border-[var(--color-tertiary)]/20">
            <span className="w-2 h-2 rounded-full bg-[var(--color-tertiary)] animate-pulse"></span>
            LIVE TELEMETRY v2.4
          </span>
        </div>
        <nav className="hidden md:flex gap-[16px] h-full items-center">
          <a href="#" className="font-body-md h-full flex items-center px-2 text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors duration-200">Analysis</a>
          <a href="#" className="font-body-md h-full flex items-center px-2 text-[var(--color-primary)] font-bold border-b-2 border-[var(--color-primary)] pb-[2px] transition-colors duration-200">Simulator</a>
          <a href="#" className="font-body-md h-full flex items-center px-2 text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors duration-200">Scouting</a>
          <a href="#" className="font-body-md h-full flex items-center px-2 text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors duration-200">Library</a>
        </nav>
        <div className="flex items-center gap-[16px]">
          <button className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors spring-physics hover:scale-110">
            <span className="material-symbols-outlined">notifications</span>
          </button>
          <button className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors spring-physics hover:scale-110">
            <span className="material-symbols-outlined">settings</span>
          </button>
          <div className="w-8 h-8 rounded-full bg-[var(--color-surface-variant)] border border-[#ffffff14] overflow-hidden ml-[8px] cursor-pointer">
            <div className="w-full h-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-inverse-primary)] flex items-center justify-center">
              <span className="text-xs font-bold text-[var(--color-on-primary)]">SC</span>
            </div>
          </div>
        </div>
      </header>

      <div className="flex flex-1 pt-16 overflow-hidden">
        {/* ===== SideNavBar ===== */}
        <aside className="hidden md:flex flex-col fixed left-0 top-16 bottom-0 z-40 w-64 bg-[#111827b8] backdrop-blur-2xl border-r border-[#ffffff14] shadow-lg shadow-[#3b82f666]/10 overflow-y-auto">
          <div className="p-[24px] border-b border-[#ffffff14]">
            <h3 className="font-headline-md text-[var(--color-primary)] mb-1">Sim Engine</h3>
            <p className="font-stats-md text-[var(--color-text-secondary)]">Defensive Phase Analysis</p>
          </div>
          <div className="p-[24px] flex flex-col gap-[24px]">
            {/* Defensive AI Block */}
            <div className="flex flex-col gap-[16px]">
              <h4 className="font-label-sm text-[var(--color-text-muted)] uppercase tracking-widest">Defensive AI Block</h4>
              <div className="flex bg-[var(--color-surface-container)] rounded-lg p-1 border border-[#ffffff14]">
                {(['low', 'mid', 'high'] as const).map((block) => (
                  <button
                    key={block}
                    onClick={() => setDefensiveBlock(block)}
                    className={`flex-1 py-1 px-2 font-label-sm rounded-md transition-colors ${
                      defensiveBlock === block
                        ? 'bg-[var(--color-primary-container)]/20 text-[var(--color-primary)] border border-[var(--color-primary)]/30 glow-active'
                        : 'text-[var(--color-text-secondary)] hover:text-[var(--color-primary)]'
                    }`}
                  >
                    {block.charAt(0).toUpperCase() + block.slice(1)}
                  </button>
                ))}
              </div>
              <div className="flex flex-col gap-2 mt-2">
                <div className="flex justify-between items-center">
                  <span className="font-label-sm text-[var(--color-text-secondary)]">Horizontal Shift</span>
                  <span className="font-stats-md text-[var(--color-primary)]">{horizontalShift}%</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="100"
                  value={horizontalShift}
                  onChange={(e) => setHorizontalShift(Number(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="flex flex-col gap-2">
                <div className="flex justify-between items-center">
                  <span className="font-label-sm text-[var(--color-text-secondary)]">Vertical Compactness</span>
                  <span className="font-stats-md text-[var(--color-primary)]">{verticalCompactness}m</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="100"
                  value={verticalCompactness}
                  onChange={(e) => setVerticalCompactness(Number(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>

            {/* Visual Overlays */}
            <div className="flex flex-col gap-[16px] mt-4 border-t border-[#ffffff14] pt-[24px]">
              <h4 className="font-label-sm text-[var(--color-text-muted)] uppercase tracking-widest">Visual Overlays</h4>

              {[
                { label: 'Voronoi Tessellation', state: showVoronoi, setter: setShowVoronoi },
                { label: 'Vision Cones', state: showVisionCones, setter: setShowVisionCones },
                { label: 'Pressure Heatmap', state: showHeatmap, setter: setShowHeatmap },
                { label: 'Análisis de Espacios', state: showSpaceAnalysis, setter: setShowSpaceAnalysis },
              ].map(({ label, state, setter }) => (
                <label key={label} className="flex items-center justify-between cursor-pointer group">
                  <span className="font-body-md text-[var(--color-text-secondary)] group-hover:text-[var(--color-text-primary)] transition-colors">{label}</span>
                  <div className="relative">
                    <input
                      type="checkbox"
                      checked={state}
                      onChange={() => setter(!state)}
                      className="sr-only"
                    />
                    <div className="block bg-[var(--color-surface-container)] w-10 h-6 rounded-full border border-[#ffffff14]"></div>
                    <div
                      className={`dot absolute left-1 top-1 w-4 h-4 rounded-full transition transform ${
                        state
                          ? 'bg-[var(--color-primary)] translate-x-4 shadow-[0_0_8px_rgba(77,142,255,0.6)]'
                          : 'bg-[var(--color-surface-variant)]'
                      }`}
                    ></div>
                  </div>
                </label>
              ))}
            </div>
          </div>
          <div className="mt-auto p-[24px]">
            <button className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg bg-gradient-to-r from-[var(--color-primary-container)] to-[var(--color-inverse-primary)] text-[var(--color-text-primary)] font-label-sm border border-[var(--color-primary)]/50 spring-physics hover:scale-[0.98] glow-active">
              <span className="material-symbols-outlined text-[18px]">rocket_launch</span>
              Launch Simulation
            </button>
          </div>
        </aside>

        {/* ===== Central Area: Tactical Pitch ===== */}
        <main className="flex-1 ml-0 md:ml-64 relative bg-[var(--color-canvas)] pitch-grid flex items-center justify-center mb-20 md:mb-24">
          {/* Floating HUD (Right) */}
          <div className="absolute right-[24px] top-[24px] flex flex-col gap-[16px] z-20 w-64 pointer-events-none">
            {/* KPI Card 1: Line Distance */}
            <div className="glass-panel p-4 pointer-events-auto spring-physics hover:border-[var(--color-primary)]/30">
              <h5 className="font-label-sm text-[var(--color-text-muted)] uppercase mb-1">Line Distance</h5>
              <div className="flex items-end gap-2">
                <span className="font-headline-lg text-[var(--color-text-primary)] leading-none">18.4</span>
                <span className="font-stats-md text-[var(--color-text-secondary)] mb-1">m</span>
              </div>
              <div className="mt-2 h-1 w-full bg-[var(--color-surface-container)] rounded-full overflow-hidden">
                <div className="h-full bg-[var(--color-tertiary)] w-3/4 rounded-full shadow-[0_0_8px_rgba(78,222,163,0.6)]"></div>
              </div>
            </div>

            {/* KPI Card 2: Defensive xG */}
            <div className="glass-panel p-4 pointer-events-auto spring-physics hover:border-[var(--color-primary)]/30">
              <h5 className="font-label-sm text-[var(--color-text-muted)] uppercase mb-1">Defensive xG</h5>
              <div className="flex items-end gap-2">
                <span className="font-headline-lg text-[var(--color-text-primary)] leading-none">0.12</span>
              </div>
              <div className="mt-2 flex gap-1">
                <div className="h-1 flex-1 bg-[var(--color-tertiary)] rounded-full shadow-[0_0_8px_rgba(78,222,163,0.6)]"></div>
                <div className="h-1 flex-1 bg-[var(--color-surface-container)] rounded-full"></div>
                <div className="h-1 flex-1 bg-[var(--color-surface-container)] rounded-full"></div>
              </div>
            </div>

            {/* KPI Card 3: Ocupación de Espacios */}
            <div className="glass-panel p-4 pointer-events-auto spring-physics hover:border-[var(--color-primary)]/30">
              <h5 className="font-label-sm text-[var(--color-text-muted)] uppercase mb-2">Ocupación de Espacios</h5>
              <div className="flex items-center justify-between mb-3">
                <span className="font-headline-md text-[var(--color-primary)]">Alta</span>
                <span
                  className="material-symbols-outlined text-[var(--color-primary)]"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  stacked_line_chart
                </span>
              </div>
              <div className="flex flex-col gap-2 border-t border-[#ffffff14] pt-2">
                <div className="flex justify-between items-center">
                  <span className="font-label-sm text-[var(--color-text-secondary)]">Mapa de Densidad</span>
                  <div className="flex gap-1">
                    <div className="w-2 h-2 rounded-full bg-[var(--color-primary)]"></div>
                    <div className="w-2 h-2 rounded-full bg-[var(--color-primary)]/60"></div>
                    <div className="w-2 h-2 rounded-full bg-[var(--color-primary)]/30"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-label-sm text-[var(--color-text-secondary)]">Canales de Progresión</span>
                  <span className="font-stats-md text-[var(--color-primary)] font-bold">74%</span>
                </div>
                <div className="h-1 w-full bg-[var(--color-surface-container)] rounded-full overflow-hidden">
                  <div className="h-full bg-[var(--color-primary)] w-[74%] rounded-full shadow-[0_0_8px_rgba(77,142,255,0.5)]"></div>
                </div>
              </div>
            </div>
          </div>

          {/* Pitch Container */}
          <div className="relative w-[800px] h-[500px] max-w-[95%] transform rotate-x-12 scale-95 md:scale-100 transition-transform duration-500">
            {/* SVG Pitch Lines */}
            <svg className="w-full h-full absolute inset-0 pointer-events-none" viewBox="0 0 100 65">
              <rect className="pitch-lines" height="65" width="100" x="0" y="0" />
              <line className="pitch-lines" x1="50" x2="50" y1="0" y2="65" />
              <circle className="pitch-lines" cx="50" cy="32.5" r="9.15" />
              <circle cx="50" cy="32.5" fill="rgba(255,255,255,0.3)" r="0.5" />
              {/* Penalty Areas */}
              <rect className="pitch-lines" height="37.32" width="16.5" x="0" y="13.84" />
              <rect className="pitch-lines" height="37.32" width="16.5" x="83.5" y="13.84" />
              {/* Goal Areas */}
              <rect className="pitch-lines" height="15.32" width="5.5" x="0" y="24.84" />
              <rect className="pitch-lines" height="15.32" width="5.5" x="94.5" y="24.84" />
            </svg>

            {/* Pass Lines (Overlay) */}
            <svg className="w-full h-full absolute inset-0 pointer-events-none z-10" viewBox="0 0 800 500">
              <defs>
                <linearGradient id="pass-grad" x1="0%" x2="100%" y1="0%" y2="100%">
                  <stop offset="0%" stopColor="#4edea3" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#4edea3" stopOpacity="0.1" />
                </linearGradient>
              </defs>
              <line className="animate-[dash_1s_linear_infinite]" stroke="url(#pass-grad)" strokeDasharray="4 4" strokeWidth="2" x1="240" x2="400" y1="200" y2="350" />
              <line stroke="#f59e0b" strokeOpacity="0.6" strokeWidth="1.5" x1="400" x2="550" y1="350" y2="280" />
              <line opacity="0.4" stroke="#4edea3" strokeDasharray="2 2" strokeWidth="1" x1="160" x2="240" y1="150" y2="150" />
              <line opacity="0.4" stroke="#ef4444" strokeDasharray="2 2" strokeWidth="1" x1="240" x2="400" y1="350" y2="200" />
              <line opacity="0.4" stroke="#f59e0b" strokeDasharray="2 2" strokeWidth="1" x1="520" x2="560" y1="275" y2="150" />
            </svg>

            {/* Voronoi/Zones Mock (CSS based) */}
            <div className="absolute inset-0 pointer-events-none opacity-20 z-0 flex">
              <div className="w-1/3 h-full bg-[var(--color-threat-red)] blur-3xl rounded-full translate-x-1/4"></div>
              <div className="w-1/3 h-full bg-[var(--color-primary)] blur-3xl rounded-full translate-x-3/4"></div>
              {showSpaceAnalysis && (
                <div className="absolute inset-0 grid grid-cols-6 grid-rows-4 gap-px opacity-30">
                  {[...Array(24)].map((_, i) => (
                    <div
                      key={i}
                      className="border border-[var(--color-accent-blue-glow)]/10"
                      style={{
                        backgroundColor: `rgba(59, 130, 246, ${[0.2, 0.4, 0.1, 0.2, 0.6, 0.3, 0.1, 0.2, 0.5, 0.1, 0.2, 0.4, 0.3, 0.1, 0.2, 0.6, 0.1, 0.2, 0.4, 0.1, 0.2, 0.5, 0.1, 0.3][i]} / 1)`,
                      }}
                    ></div>
                  ))}
                </div>
              )}
            </div>

            {/* Defensive Nodes (Green/Emerald) */}
            {players.filter((p) => p.team === 'def').map((player) => (
              <div
                key={player.id}
                className="tactical-node node-def z-20"
                style={{ left: `${player.x}%`, top: `${player.y}%` }}
              >
                {player.name}
              </div>
            ))}

            {/* Attacking Nodes (Red) */}
            {players.filter((p) => p.team === 'att').map((player) => (
              <div
                key={player.id}
                className="tactical-node node-att z-20"
                style={{ left: `${player.x}%`, top: `${player.y}%` }}
              >
                {player.name}
              </div>
            ))}

            {/* Ball */}
            <div
              className="absolute w-4 h-4 bg-white rounded-full z-30 shadow-[0_0_10px_rgba(255,255,255,0.8)]"
              style={{ left: '68%', top: '56%' }}
            ></div>

            {/* Heatmap overlay */}
            {showHeatmap && (
              <div className="absolute inset-0 pointer-events-none opacity-20 z-0 flex">
                <div className="w-1/3 h-full bg-[var(--color-threat-red)] blur-3xl rounded-full translate-x-1/4"></div>
                <div className="w-1/3 h-full bg-[var(--color-primary)] blur-3xl rounded-full translate-x-3/4"></div>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* ===== BottomNavBar (Timeline & Playback) ===== */}
      <footer className="fixed bottom-0 left-0 md:left-64 right-0 z-50 flex flex-col justify-center bg-[#111827b8] backdrop-blur-xl border-t border-[#ffffff14] px-[24px] py-4 rounded-t-xl">
        {/* Timeline Slider */}
        <div className="w-full flex items-center gap-[8px] mb-4">
          <span className="font-stats-md text-[var(--color-text-secondary)] w-12 text-right">{currentTime}</span>
          <div
            className="flex-1 relative h-6 flex items-center group cursor-pointer"
            onClick={handleTimelineClick}
          >
            <div className="absolute w-full h-1 bg-[var(--color-surface-container)] rounded-full"></div>
            <div
              className="absolute h-1 bg-[var(--color-primary)] rounded-full shadow-[0_0_8px_rgba(77,142,255,0.5)]"
              style={{ width: `${timelineProgress}%` }}
            ></div>
            {/* Keyframes */}
            <div className="absolute w-2 h-4 bg-[var(--color-tertiary)] rounded-sm left-[20%] -mt-1 group-hover:scale-110 transition-transform"></div>
            <div className="absolute w-2 h-4 bg-[var(--color-warning-amber)] rounded-sm left-[45%] -mt-1 shadow-[0_0_5px_rgba(245,158,11,0.8)] scale-125 z-10"></div>
            <div className="absolute w-2 h-4 bg-[var(--color-tertiary)] rounded-sm left-[75%] -mt-1 group-hover:scale-110 transition-transform"></div>
            {/* Playhead */}
            <div
              className="absolute w-4 h-4 bg-white rounded-full -ml-2 shadow-lg z-20 transition-transform scale-100 group-hover:scale-125 border-2 border-[var(--color-primary)]"
              style={{ left: `${timelineProgress}%` }}
            ></div>
          </div>
          <span className="font-stats-md text-[var(--color-text-secondary)] w-12">00:30</span>
        </div>

        {/* Controls */}
        <div className="flex justify-between items-center w-full">
          <div className="flex gap-4">
            <button className="flex flex-col items-center justify-center text-[var(--color-on-surface-variant)] hover:bg-[var(--color-surface-bright)]/20 p-2 rounded-xl transition-all spring-physics active:scale-95">
              <span className="material-symbols-outlined text-[24px]">settings_backup_restore</span>
              <span className="font-label-sm mt-1">Rewind</span>
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="flex flex-col items-center justify-center bg-[var(--color-tertiary-container)]/20 text-[var(--color-tertiary)] rounded-xl p-2 px-4 shadow-[0_0_15px_rgba(78,222,163,0.15)] border border-[var(--color-tertiary)]/30 transition-all spring-physics hover:bg-[var(--color-tertiary-container)]/30 active:scale-95"
            >
              <span
                className="material-symbols-outlined text-[28px]"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                {isPlaying ? 'pause' : 'play_arrow'}
              </span>
              <span className="font-label-sm mt-1 font-bold">{isPlaying ? 'Pause' : 'Play'}</span>
            </button>
            <button className="flex flex-col items-center justify-center text-[var(--color-on-surface-variant)] hover:bg-[var(--color-surface-bright)]/20 p-2 rounded-xl transition-all spring-physics active:scale-95">
              <span className="material-symbols-outlined text-[24px]">fast_forward</span>
              <span className="font-label-sm mt-1">Play</span>
            </button>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-[var(--color-surface-variant)]/50 hover:bg-[var(--color-surface-variant)] border border-[#ffffff14] rounded-lg text-[var(--color-text-primary)] transition-all spring-physics active:scale-95">
            <span className="material-symbols-outlined text-[20px]">save</span>
            <span className="font-label-sm">Save Play</span>
          </button>
        </div>
      </footer>

      {/* Dash animation keyframes */}
      <style>{`
        @keyframes dash {
          to { stroke-dashoffset: -8; }
        }
      `}</style>
    </div>
  );
};

export default TacticalOS;
