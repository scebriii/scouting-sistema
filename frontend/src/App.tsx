import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, Pause, FastForward, FastForwardOff, Save, 
  Settings, Bell, Search, ChevronDown, TrendingUp,
  Activity, Map, Target, Shield, Zap, Layers,
  BarChart3, PieChart, Eye, EyeOff
} from 'lucide-react';

interface Player {
  id: number;
  name: string;
  position: string;
  x: number;
  y: number;
  team: 'def' | 'att';
}

interface MatchData {
  rival: string;
  sistema: string;
  estilo: string;
}

const TacticalOS: React.FC = () => {
  const [matchData, setMatchData] = useState<MatchData>({
    rival: 'Real Madrid',
    sistema: '4-3-3',
    estilo: 'Posesión alta'
  });
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [showVoronoi, setShowVoronoi] = useState(true);
  const [showVisionCones, setShowVisionCones] = useState(false);
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [showSpaceAnalysis, setShowSpaceAnalysis] = useState(false);
  const [defensiveBlock, setDefensiveBlock] = useState<'low' | 'mid' | 'high'>('mid');
  const [horizontalShift, setHorizontalShift] = useState(68);
  const [verticalCompactness, setVerticalCompactness] = useState(42);
  const [timelineProgress, setTimelineProgress] = useState(45);
  const [currentTime, setCurrentTime] = useState('00:14');
  const [totalTime, setTotalTime] = useState('00:30');

  const players: Player[] = [
    // Defensivos
    { id: 1, name: '4', position: 'LD', x: 20, y: 30, team: 'def' },
    { id: 2, name: '3', position: 'LI', x: 20, y: 70, team: 'def' },
    { id: 3, name: '5', position: 'CD', x: 30, y: 50, team: 'def' },
    { id: 4, name: '8', position: 'MC', x: 45, y: 40, team: 'def' },
    // Atacantes
    { id: 5, name: '9', position: 'DC', x: 50, y: 70, team: 'att' },
    { id: 6, name: '10', position: 'MCO', x: 65, y: 55, team: 'att' },
    { id: 7, name: '7', position: 'EI', x: 70, y: 30, team: 'att' },
  ];

  const handlePlayerClick = (player: Player) => {
    setSelectedPlayer(player);
  };

  const handleTimelineClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = (x / rect.width) * 100;
    setTimelineProgress(percentage);
  };

  return (
    <div className="min-h-screen bg-tactical-dark text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-tactical-glass backdrop-blur-xl border-b border-white/10">
        <div className="flex items-center justify-between px-6 py-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Zap className="w-7 h-7 text-tactical-primary" />
              <h1 className="text-2xl font-bold text-tactical-primary">TacticalOS</h1>
            </div>
            <div className="flex items-center space-x-2 px-3 py-1 bg-tactical-tertiary/10 rounded-full border border-tactical-tertiary/20">
              <div className="w-2 h-2 rounded-full bg-tactical-tertiary animate-pulse-slow"></div>
              <span className="text-sm font-medium text-tactical-tertiary">LIVE TELEMETRY v2.4</span>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#" className="text-gray-400 hover:text-white transition-colors">Analysis</a>
            <a href="#" className="text-tactical-primary font-semibold border-b-2 border-tactical-primary pb-1">Simulator</a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">Scouting</a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">Library</a>
          </nav>
          
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-white transition-colors">
              <Bell className="w-5 h-5" />
            </button>
            <button className="p-2 text-gray-400 hover:text-white transition-colors">
              <Settings className="w-5 h-5" />
            </button>
            <div className="w-8 h-8 rounded-full bg-gray-700 border border-white/20 flex items-center justify-center">
              <span className="text-sm">U</span>
            </div>
          </div>
        </div>
      </header>

      <div className="flex pt-20">
        {/* Sidebar */}
        <aside className="fixed left-0 top-20 bottom-0 w-64 bg-tactical-glass backdrop-blur-2xl border-r border-white/10 overflow-y-auto">
          <div className="p-6 border-b border-white/10">
            <h3 className="text-lg font-semibold text-tactical-primary mb-1">Sim Engine</h3>
            <p className="text-sm text-gray-400">Defensive Phase Analysis</p>
          </div>
          
          <div className="p-6 space-y-6">
            <div>
              <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">Defensive AI Block</h4>
              <div className="flex bg-tactical-surface rounded-lg p-1 border border-white/10">
                <button 
                  onClick={() => setDefensiveBlock('low')}
                  className={`flex-1 py-1 px-2 text-xs font-medium rounded-md transition-colors ${
                    defensiveBlock === 'low' ? 'bg-tactical-primary/20 text-tactical-primary border border-tactical-primary/30' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Low
                </button>
                <button 
                  onClick={() => setDefensiveBlock('mid')}
                  className={`flex-1 py-1 px-2 text-xs font-medium rounded-md transition-colors ${
                    defensiveBlock === 'mid' ? 'bg-tactical-primary/20 text-tactical-primary border border-tactical-primary/30' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Mid
                </button>
                <button 
                  onClick={() => setDefensiveBlock('high')}
                  className={`flex-1 py-1 px-2 text-xs font-medium rounded-md transition-colors ${
                    defensiveBlock === 'high' ? 'bg-tactical-primary/20 text-tactical-primary border border-tactical-primary/30' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  High
                </button>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Horizontal Shift</span>
                <span className="text-sm font-medium text-tactical-primary">{horizontalShift}%</span>
              </div>
              <input
                type="range"
                min="1"
                max="100"
                value={horizontalShift}
                onChange={(e) => setHorizontalShift(Number(e.target.value))}
                className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Vertical Compactness</span>
                <span className="text-sm font-medium text-tactical-primary">{verticalCompactness}m</span>
              </div>
              <input
                type="range"
                min="1"
                max="100"
                value={verticalCompactness}
                onChange={(e) => setVerticalCompactness(Number(e.target.value))}
                className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer"
              />
            </div>
            
            <div className="space-y-3 pt-4 border-t border-white/10">
              <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wider">Visual Overlays</h4>
              
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-gray-400">Voronoi Tessellation</span>
                <input
                  type="checkbox"
                  checked={showVoronoi}
                  onChange={() => setShowVoronoi(!showVoronoi)}
                  className="sr-only"
                />
                <div className={`w-10 h-6 rounded-full transition-colors ${showVoronoi ? 'bg-tactical-primary' : 'bg-gray-700'}`}>
                  <div className={`w-4 h-4 rounded-full bg-white transition-transform mt-1 ${showVoronoi ? 'translate-x-5' : 'translate-x-1'}`}></div>
                </div>
              </label>
              
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-gray-400">Vision Cones</span>
                <input
                  type="checkbox"
                  checked={showVisionCones}
                  onChange={() => setShowVisionCones(!showVisionCones)}
                  className="sr-only"
                />
                <div className={`w-10 h-6 rounded-full transition-colors ${showVisionCones ? 'bg-tactical-primary' : 'bg-gray-700'}`}>
                  <div className={`w-4 h-4 rounded-full bg-white transition-transform mt-1 ${showVisionCones ? 'translate-x-5' : 'translate-x-1'}`}></div>
                </div>
              </label>
              
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-gray-400">Pressure Heatmap</span>
                <input
                  type="checkbox"
                  checked={showHeatmap}
                  onChange={() => setShowHeatmap(!showHeatmap)}
                  className="sr-only"
                />
                <div className={`w-10 h-6 rounded-full transition-colors ${showHeatmap ? 'bg-tactical-primary' : 'bg-gray-700'}`}>
                  <div className={`w-4 h-4 rounded-full bg-white transition-transform mt-1 ${showHeatmap ? 'translate-x-5' : 'translate-x-1'}`}></div>
                </div>
              </label>
              
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-gray-400">Análisis de Espacios</span>
                <input
                  type="checkbox"
                  checked={showSpaceAnalysis}
                  onChange={() => setShowSpaceAnalysis(!showSpaceAnalysis)}
                  className="sr-only"
                />
                <div className={`w-10 h-6 rounded-full transition-colors ${showSpaceAnalysis ? 'bg-tactical-primary' : 'bg-gray-700'}`}>
                  <div className={`w-4 h-4 rounded-full bg-white transition-transform mt-1 ${showSpaceAnalysis ? 'translate-x-5' : 'translate-x-1'}`}></div>
                </div>
              </label>
            </div>
          </div>
          
          <div className="p-6 mt-auto">
            <button className="w-full flex items-center justify-center space-x-2 py-2 px-4 rounded-lg bg-gradient-to-r from-tactical-primary to-blue-600 text-white font-medium text-sm border border-tactical-primary/50 hover:scale-[0.98] transition-transform glow-primary">
              <Zap className="w-4 h-4" />
              <span>Launch Simulation</span>
            </button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 ml-64 relative">
          {/* Match Info */}
          <div className="absolute top-6 right-6 z-20 w-64 space-y-4">
            <div className="glass-panel p-4">
              <h5 className="text-xs font-medium text-gray-500 uppercase mb-2">Line Distance</h5>
              <div className="flex items-end space-x-2">
                <span className="text-2xl font-bold text-white">18.4</span>
                <span className="text-sm text-gray-400 mb-1">m</span>
              </div>
              <div className="mt-2 h-1 w-full bg-gray-700 rounded-full overflow-hidden">
                <div className="h-full bg-tactical-tertiary w-3/4 rounded-full glow-tertiary"></div>
              </div>
            </div>
            
            <div className="glass-panel p-4">
              <h5 className="text-xs font-medium text-gray-500 uppercase mb-2">Defensive xG</h5>
              <div className="flex items-end space-x-2">
                <span className="text-2xl font-bold text-white">0.12</span>
              </div>
              <div className="mt-2 flex space-x-1">
                <div className="h-1 flex-1 bg-tactical-tertiary rounded-full glow-tertiary"></div>
                <div className="h-1 flex-1 bg-gray-700 rounded-full"></div>
                <div className="h-1 flex-1 bg-gray-700 rounded-full"></div>
              </div>
            </div>
            
            <div className="glass-panel p-4">
              <h5 className="text-xs font-medium text-gray-500 uppercase mb-3">Ocupación de Espacios</h5>
              <div className="flex items-center justify-between mb-3">
                <span className="text-lg font-semibold text-tactical-primary">Alta</span>
                <TrendingUp className="w-5 h-5 text-tactical-primary" />
              </div>
              <div className="space-y-2 border-t border-white/10 pt-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-400">Mapa de Densidad</span>
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 rounded-full bg-tactical-primary"></div>
                    <div className="w-2 h-2 rounded-full bg-tactical-primary/60"></div>
                    <div className="w-2 h-2 rounded-full bg-tactical-primary/30"></div>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-400">Canales de Progresión</span>
                  <span className="text-sm font-bold text-tactical-primary">74%</span>
                </div>
                <div className="h-1 w-full bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-tactical-primary w-[74%] rounded-full" style={{boxShadow: '0 0 8px rgba(77, 142, 255, 0.5)'}}></div>
                </div>
              </div>
            </div>
          </div>

          {/* Tactical Pitch */}
          <div className="flex items-center justify-center min-h-[600px] p-8">
            <div className="relative w-full max-w-4xl aspect-[16/10] bg-gradient-to-br from-green-800/20 to-green-900/30 rounded-xl border border-white/10 overflow-hidden">
              {/* Pitch Grid */}
              <div className="absolute inset-0 opacity-20">
                <div className="grid grid-cols-8 grid-rows-6 h-full">
                  {Array.from({ length: 48 }).map((_, i) => (
                    <div key={i} className="border border-white/5"></div>
                  ))}
                </div>
              </div>
              
              {/* Pitch Lines */}
              <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 65">
                <rect fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" width="100" height="65" />
                <line x1="50" y1="0" x2="50" y2="65" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" />
                <circle cx="50" cy="32.5" r="9.15" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" />
                <circle cx="50" cy="32.5" r="0.5" fill="rgba(255,255,255,0.3)" />
                <rect x="0" y="13.84" width="16.5" height="37.32" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" />
                <rect x="83.5" y="13.84" width="16.5" height="37.32" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" />
                <rect x="0" y="24.84" width="5.5" height="15.32" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" />
                <rect x="94.5" y="24.84" width="5.5" height="15.32" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" />
              </svg>
              
              {/* Pass Lines */}
              <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 65">
                <line x1="20" y1="30" x2="50" y2="70" stroke="rgba(78,222,163,0.6)" strokeWidth="0.3" strokeDasharray="2 2" />
                <line x1="50" y1="70" x2="70" y2="30" stroke="rgba(245,158,11,0.4)" strokeWidth="0.2" />
                <line x1="20" y1="30" x2="30" y2="50" stroke="rgba(78,222,163,0.3)" strokeWidth="0.2" strokeDasharray="1 1" />
              </svg>
              
              {/* Players */}
              {players.map((player) => (
                <div
                  key={player.id}
                  className={`tactical-node ${player.team === 'def' ? 'node-def' : 'node-att'}`}
                  style={{
                    left: `${player.x}%`,
                    top: `${player.y}%`,
                    transform: 'translate(-50%, -50%)'
                  }}
                  onClick={() => handlePlayerClick(player)}
                >
                  {player.name}
                </div>
              ))}
              
              {/* Ball */}
              <div 
                className="absolute w-3 h-3 bg-white rounded-full z-30"
                style={{
                  left: '68%',
                  top: '56%',
                  transform: 'translate(-50%, -50%)',
                  boxShadow: '0 0 10px rgba(255,255,255,0.8)'
                }}
              ></div>
              
              {/* Heatmap Overlay */}
              {showHeatmap && (
                <div className="absolute inset-0 opacity-30">
                  <div className="absolute top-1/4 left-1/4 w-1/3 h-1/3 bg-red-500/20 rounded-full blur-xl"></div>
                  <div className="absolute top-1/2 left-1/2 w-1/4 h-1/4 bg-blue-500/20 rounded-full blur-xl"></div>
                  <div className="absolute bottom-1/4 right-1/4 w-1/5 h-1/5 bg-emerald-500/20 rounded-full blur-xl"></div>
                </div>
              )}
              
              {/* Space Analysis Overlay */}
              {showSpaceAnalysis && (
                <div className="absolute inset-0 opacity-40">
                  <div className="grid grid-cols-6 grid-rows-4 h-full">
                    {Array.from({ length: 24 }).map((_, i) => (
                      <div 
                        key={i} 
                        className={`border border-tactical-primary/20 ${
                          i % 3 === 0 ? 'bg-tactical-primary/10' : 
                          i % 3 === 1 ? 'bg-tactical-primary/5' : ''
                        }`}
                      ></div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Timeline Footer */}
      <footer className="fixed bottom-0 left-0 right-0 z-50 bg-tactical-glass backdrop-blur-xl border-t border-white/10 px-6 py-4">
        <div className="flex items-center space-x-4 mb-4">
          <span className="text-sm font-mono text-gray-400 w-12 text-right">{currentTime}</span>
          <div 
            className="flex-1 relative h-6 flex items-center cursor-pointer"
            onClick={handleTimelineClick}
          >
            <div className="absolute w-full h-1 bg-gray-700 rounded-full"></div>
            <div 
              className="absolute h-1 bg-tactical-primary rounded-full"
              style={{ width: `${timelineProgress}%`, boxShadow: '0 0 8px rgba(77, 142, 255, 0.5)' }}
            ></div>
            <div 
              className="absolute w-2 h-4 bg-tactical-tertiary rounded-sm -mt-1"
              style={{ left: '20%' }}
            ></div>
            <div 
              className="absolute w-2 h-4 bg-tactical-warning rounded-sm -mt-1 shadow-lg z-10"
              style={{ left: `${timelineProgress}%` }}
            ></div>
            <div 
              className="absolute w-4 h-4 bg-white rounded-full -ml-2 shadow-lg z-20"
              style={{ left: `${timelineProgress}%` }}
            ></div>
          </div>
          <span className="text-sm font-mono text-gray-400 w-12">{totalTime}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <div className="flex space-x-4">
            <button className="flex flex-col items-center justify-center text-gray-400 hover:text-white p-2 rounded-xl transition-colors hover:bg-white/10">
              <FastForwardOff className="w-6 h-6" />
              <span className="text-xs mt-1">Rewind</span>
            </button>
            <button 
              onClick={() => setIsPlaying(!isPlaying)}
              className="flex flex-col items-center justify-center bg-tactical-tertiary/20 text-tactical-tertiary rounded-xl p-2 px-4 shadow-lg border border-tactical-tertiary/30 transition-all hover:bg-tactical-tertiary/30"
            >
              {isPlaying ? (
                <Pause className="w-7 h-7" />
              ) : (
                <Play className="w-7 h-7" />
              )}
              <span className="text-xs mt-1 font-semibold">{isPlaying ? 'Pause' : 'Play'}</span>
            </button>
            <button className="flex flex-col items-center justify-center text-gray-400 hover:text-white p-2 rounded-xl transition-colors hover:bg-white/10">
              <FastForward className="w-6 h-6" />
              <span className="text-xs mt-1">Play</span>
            </button>
          </div>
          
          <button className="flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-white transition-colors">
            <Save className="w-5 h-5" />
            <span className="text-sm font-medium">Save Play</span>
          </button>
        </div>
      </footer>
    </div>
  );
};

export default TacticalOS;
