import React from 'react';
import { motion } from 'framer-motion';
import { 
  Users, GitBranch, Star, MapPin, Calendar, 
  Award, Briefcase, Zap, BrainCircuit, Target, Code
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';

// --- Simple Reusable UI Components ---
const Card = ({ children, className = '', title }) => (
  <div className={`glass-card ${className}`}>
    {title && <h3 className="text-lg font-semibold mb-4 text-white/90">{title}</h3>}
    {children}
  </div>
);

const Badge = ({ children, color = 'primary' }) => {
  const colors = {
    primary: 'bg-primary/20 text-primary border-primary/30',
    secondary: 'bg-secondary/20 text-secondary border-secondary/30',
    success: 'bg-success/20 text-success border-success/30',
    gray: 'bg-white/10 text-gray-300 border-white/20'
  };
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${colors[color] || colors.primary}`}>
      {children}
    </span>
  );
};

// --- Sub-components for Dashboard ---
const ProfileOverview = ({ profile, score, level }) => (
  <Card className="col-span-1 md:col-span-1 lg:col-span-3 bg-gradient-to-br from-card/80 to-primary/5">
    <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
      <div className="relative">
        <img 
          src={profile.avatar_url} 
          alt={profile.username} 
          className="w-24 h-24 rounded-full border-2 border-primary/50 shadow-[0_0_20px_rgba(99,102,241,0.3)]"
        />
        <div className="absolute -bottom-2 -right-2 bg-background border border-primary/30 text-xs px-2 py-1 rounded-lg font-bold text-primary">
          {score}/100
        </div>
      </div>
      
      <div className="flex-1 text-center md:text-left">
        <h2 className="text-2xl font-bold text-white mb-1">{profile.name || profile.username}</h2>
        <div className="text-primary font-medium mb-3">@{profile.username} • {level}</div>
        <p className="text-gray-400 text-sm max-w-2xl mb-4 leading-relaxed">
          {profile.bio || "No bio provided."}
        </p>
        
        <div className="flex flex-wrap items-center justify-center md:justify-start gap-4 text-sm text-gray-500">
          {profile.location && <div className="flex items-center"><MapPin size={14} className="mr-1"/> {profile.location}</div>}
          <div className="flex items-center"><Users size={14} className="mr-1"/> {profile.followers} followers</div>
          <div className="flex items-center"><GitBranch size={14} className="mr-1"/> {profile.public_repos} repos</div>
        </div>
      </div>
    </div>
  </Card>
);

const MetricCard = ({ title, value, icon: Icon, colorClass }) => (
  <Card className="flex items-center gap-4 hover:bg-white/5 cursor-default">
    <div className={`p-3 rounded-xl ${colorClass}`}>
      <Icon size={24} />
    </div>
    <div>
      <div className="text-gray-400 text-sm">{title}</div>
      <div className="text-2xl font-bold text-white">{value}</div>
    </div>
  </Card>
);

const AIAnalysis = ({ insights }) => (
  <Card title="AI Developer Analysis" className="h-full">
    <div className="space-y-6">
      <div>
        <p className="text-gray-300 text-sm leading-relaxed border-l-2 border-primary pl-4 italic">
          "{insights.summary}"
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 className="flex items-center text-sm font-medium text-success mb-3"><Target size={16} className="mr-2"/> Strengths</h4>
          <ul className="space-y-2">
            {insights.strengths.map((s, i) => (
              <li key={i} className="text-sm text-gray-400 flex items-start"><span className="mr-2 text-success mt-0.5">•</span> {s}</li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="flex items-center text-sm font-medium text-secondary mb-3"><BrainCircuit size={16} className="mr-2"/> Technical Focus</h4>
          <ul className="space-y-2">
            {insights.technical_focus.map((t, i) => (
              <li key={i} className="text-sm text-gray-400 flex items-start"><span className="mr-2 text-secondary mt-0.5">•</span> {t}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  </Card>
);

const ScoreCard = ({ scores }) => {
  const radarData = [
    { subject: 'Technical', A: scores.score_technical, fullMark: 100 },
    { subject: 'Quality', A: scores.score_quality, fullMark: 100 },
    { subject: 'Consistency', A: scores.score_consistency, fullMark: 100 },
    { subject: 'Impact', A: scores.score_impact, fullMark: 100 },
    { subject: 'Portfolio', A: scores.score_portfolio, fullMark: 100 },
  ];

  return (
    <Card title="Recruiter Scorecard" className="flex flex-col items-center">
      <div className="w-full h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
            <PolarGrid stroke="#374151" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
            <Radar name="Score" dataKey="A" stroke="#6366F1" fill="#6366F1" fillOpacity={0.4} />
            <Tooltip contentStyle={{ backgroundColor: '#111827', borderColor: '#374151' }} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

// --- Main Dashboard Layout ---
export default function Dashboard({ data }) {
  const pieColors = ['#6366F1', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#3B82F6'];
  const langData = Object.entries(data.languages)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 6);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Top Row: Profile & Overview */}
      <ProfileOverview profile={data.profile} score={data.overall_score} level={data.developer_level} />
      
      <MetricCard title="Total Stars" value={data.profile.total_stars} icon={Star} colorClass="bg-yellow-500/10 text-yellow-500" />
      <MetricCard title="Total Forks" value={data.profile.total_forks} icon={GitBranch} colorClass="bg-blue-500/10 text-blue-500" />
      <MetricCard title="Repositories" value={data.profile.public_repos} icon={Code} colorClass="bg-green-500/10 text-green-500" />

      {/* Second Row: AI & Scores */}
      <div className="col-span-1 lg:col-span-2">
        <AIAnalysis insights={data.ai_insights} />
      </div>
      <div className="col-span-1">
        <ScoreCard scores={data} />
      </div>

      {/* Third Row: Roles & Skills */}
      <Card title="Career Recommendations" className="col-span-1">
        <div className="space-y-4">
          {data.career_recommendations.map((rec, i) => (
            <div key={i} className="flex items-center justify-between">
              <span className="text-sm font-medium text-white/90">{rec.role}</span>
              <div className="flex items-center gap-3 w-1/2">
                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${rec.confidence}%` }}
                    transition={{ duration: 1, delay: i * 0.1 }}
                    className="h-full bg-gradient-to-r from-primary to-secondary"
                  />
                </div>
                <span className="text-xs text-gray-400 w-8">{rec.confidence}%</span>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Skill Extraction" className="col-span-1 lg:col-span-2">
        <div className="flex flex-wrap gap-2">
          {Object.keys(data.languages).map((lang, i) => (
            <Badge key={i} color="primary">{lang}</Badge>
          ))}
          {data.ai_insights.technical_focus.map((focus, i) => (
            <Badge key={`f-${i}`} color="secondary">{focus}</Badge>
          ))}
        </div>
        <div className="mt-8 flex flex-col md:flex-row gap-6">
           <div className="w-full md:w-1/2 h-[200px]">
             <ResponsiveContainer width="100%" height="100%">
               <PieChart>
                 <Pie data={langData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                   {langData.map((entry, index) => <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />)}
                 </Pie>
                 <Tooltip contentStyle={{ backgroundColor: '#111827', borderColor: '#374151' }} itemStyle={{ color: '#fff' }} />
               </PieChart>
             </ResponsiveContainer>
           </div>
           <div className="w-full md:w-1/2 flex flex-col justify-center">
             <h4 className="text-sm font-medium text-gray-300 mb-4">Language Distribution</h4>
             {langData.slice(0,4).map((lang, i) => (
               <div key={i} className="flex items-center justify-between mb-2">
                 <div className="flex items-center">
                   <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: pieColors[i] }}></div>
                   <span className="text-xs text-gray-400">{lang.name}</span>
                 </div>
                 <span className="text-xs text-white font-medium">{lang.value} repos</span>
               </div>
             ))}
           </div>
        </div>
      </Card>

      <Card title="Repository Highlights" className="col-span-1 lg:col-span-2">
        <div className="flex flex-col justify-center h-full">
            <h4 className="text-sm font-medium text-gray-300 mb-3 flex items-center"><Award size={16} className="mr-2"/> Best Project</h4>
            <div className="text-sm text-gray-400 bg-primary/10 border border-primary/20 p-4 rounded-xl mb-6">
              <span className="font-semibold text-primary block mb-1">{data.repo_insights.best_project}</span>
              {data.repo_insights.best_project_reason}
            </div>

            <h4 className="text-sm font-medium text-gray-300 mb-3 flex items-center"><BrainCircuit size={16} className="mr-2"/> Most Complex Project</h4>
            <div className="text-sm text-gray-400 bg-secondary/10 border border-secondary/20 p-4 rounded-xl">
              <span className="font-semibold text-secondary block mb-1">{data.repo_insights.complex_project}</span>
              {data.repo_insights.complex_project_reason}
            </div>
        </div>
      </Card>

      <Card title="Top Repositories" className="col-span-1">
        <div className="space-y-3">
          {data.top_repos.slice(0, 4).map((repo, i) => (
            <div key={i} className="p-3 bg-white/5 rounded-xl border border-white/5 hover:border-white/10 transition-colors">
              <div className="flex justify-between items-start mb-1">
                <a href={`https://github.com/${data.profile.username}/${repo.name}`} target="_blank" rel="noreferrer" className="text-sm font-semibold text-primary hover:underline truncate mr-2">
                  {repo.name}
                </a>
                <div className="flex items-center text-xs text-gray-400 whitespace-nowrap">
                  <Star size={12} className="mr-1 text-yellow-500" /> {repo.stars}
                </div>
              </div>
              <p className="text-xs text-gray-500 line-clamp-2">{repo.description || 'No description available.'}</p>
              {repo.language && (
                <div className="mt-2 text-[10px] uppercase font-bold text-gray-400">
                  {repo.language}
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
