import { useState } from 'react';
import { Search, Loader2, Github, AlertCircle } from 'lucide-react';
import axios from 'axios';
import Dashboard from './components/Dashboard';

function App() {
  const [mode, setMode] = useState('single'); // 'single' or 'compare'
  const [username1, setUsername1] = useState('');
  const [username2, setUsername2] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data1, setData1] = useState(null);
  const [data2, setData2] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!username1.trim()) return;
    if (mode === 'compare' && !username2.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      if (mode === 'single') {
        const response = await axios.get(`${API_BASE_URL}/api/analyze/${username1}`);
        setData1(response.data);
        setData2(null);
      } else {
        const [res1, res2] = await Promise.all([
          axios.get(`${API_BASE_URL}/api/analyze/${username1}`),
          axios.get(`${API_BASE_URL}/api/analyze/${username2}`)
        ]);
        setData1(res1.data);
        setData2(res2.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-background">
      {/* Abstract Background Gradients */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[400px] bg-primary/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-1/4 right-0 w-[500px] h-[500px] bg-secondary/10 blur-[120px] rounded-full pointer-events-none" />
      
      <div className="container mx-auto px-4 py-12 relative z-10">
        {!data1 && (
          <div className="max-w-2xl mx-auto text-center mt-20">
            <div className="flex justify-center mb-6">
              <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center border border-white/10 shadow-lg">
                <Github size={32} className="text-white" />
              </div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">
              Developer <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">Intelligence</span> Platform
            </h1>
            <p className="text-gray-400 text-lg mb-10">
              Enter a GitHub username to generate an AI-powered insights dashboard, career recommendations, and technical analysis.
            </p>

            <div className="flex justify-center gap-4 mb-8">
              <button 
                onClick={() => setMode('single')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${mode === 'single' ? 'bg-primary/20 text-primary border border-primary/30' : 'text-gray-400 hover:text-white'}`}
              >
                Single Analysis
              </button>
              <button 
                onClick={() => setMode('compare')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${mode === 'compare' ? 'bg-secondary/20 text-secondary border border-secondary/30' : 'text-gray-400 hover:text-white'}`}
              >
                Compare Profiles
              </button>
            </div>

            <form onSubmit={handleSearch} className="relative max-w-2xl mx-auto flex flex-col gap-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
                  <input
                    type="text"
                    value={username1}
                    onChange={(e) => setUsername1(e.target.value)}
                    placeholder="Developer 1 (e.g. torvalds)"
                    className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all"
                  />
                </div>
                {mode === 'compare' && (
                  <div className="relative flex-1 animate-in fade-in slide-in-from-left-4">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
                    <input
                      type="text"
                      value={username2}
                      onChange={(e) => setUsername2(e.target.value)}
                      placeholder="Developer 2 (e.g. gaearon)"
                      className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-secondary/50 focus:border-transparent transition-all"
                    />
                  </div>
                )}
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full md:w-auto self-center bg-gradient-to-r from-primary to-secondary hover:opacity-90 text-white px-8 py-3 rounded-xl font-medium transition-opacity disabled:opacity-50 flex items-center justify-center"
              >
                {loading ? <Loader2 size={20} className="animate-spin mr-2" /> : null}
                {mode === 'compare' ? 'Compare Developers' : 'Analyze Developer'}
              </button>
              
              {error && (
                <div className="flex items-center justify-center text-red-400 bg-red-400/10 py-3 rounded-xl border border-red-400/20 mt-2">
                  <AlertCircle size={16} className="mr-2" />
                  <span className="text-sm">{error}</span>
                </div>
              )}
            </form>

          </div>
        )}

        {data1 && (
          <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="mb-8 flex justify-between items-center">
              <button 
                onClick={() => { setData1(null); setData2(null); }}
                className="text-gray-400 hover:text-white transition-colors flex items-center text-sm font-medium bg-white/5 px-4 py-2 rounded-lg"
              >
                ← New Search
              </button>
              <div className="flex items-center text-sm text-gray-500">
                <Github size={16} className="mr-2" /> GitHub Intelligence
              </div>
            </div>
            
            {mode === 'single' || !data2 ? (
              <Dashboard data={data1} />
            ) : (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                <div className="relative border-r-0 xl:border-r border-white/10 xl:pr-8">
                  <div className="absolute -top-4 -left-4 bg-primary/20 text-primary px-4 py-1 rounded-full text-xs font-bold uppercase tracking-wider z-10 border border-primary/30">Developer 1</div>
                  <Dashboard data={data1} />
                </div>
                <div className="relative xl:pl-8 mt-12 xl:mt-0">
                  <div className="absolute -top-4 -left-4 xl:-top-4 xl:left-8 bg-secondary/20 text-secondary px-4 py-1 rounded-full text-xs font-bold uppercase tracking-wider z-10 border border-secondary/30">Developer 2</div>
                  <Dashboard data={data2} />
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
