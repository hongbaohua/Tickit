import { useState, useEffect, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Menu, X, Moon, Sun, Search, 
  ArrowUp, ChevronRight, 
  Layout, Bookmark
} from 'lucide-react';
import chapters from './content/index.json';

const markdownFiles = import.meta.glob('./content/*.md', { query: '?raw', import: 'default' });

function App() {
  const [currentChapter, setCurrentChapter] = useState(chapters[0]);
  const [content, setContent] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const loadContent = async () => {
      const filePath = `./content/${currentChapter.file}`;
      if (markdownFiles[filePath]) {
        const mdContent = await markdownFiles[filePath]();
        setContent(mdContent as string);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    };
    loadContent();
  }, [currentChapter]);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.setAttribute('data-theme', !isDarkMode ? 'dark' : 'light');
  };

  const filteredChapters = chapters.filter(ch => 
    ch.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Split content into blocks for modular display
  const blocks = useMemo(() => {
    if (!content) return [];
    // Split by horizontal rules or major section markers
    return content.split(/\n---\n/).filter(block => block.trim().length > 0);
  }, [content]);

  return (
    <>
      {/* Mobile Toggle */}
      <button 
        className="mobile-nav-toggle"
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
      >
        {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-title">
            <Layout size={24} />
            <span>iPAS 品牌企劃</span>
          </div>
          <div className="sidebar-subtitle">數位辭典型課本</div>
        </div>
        
        <div className="search-container">
          <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', opacity: 0.4 }} />
          <input 
            type="text" 
            placeholder="搜尋知識模組..." 
            className="search-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <nav className="nav-list">
          {filteredChapters.map((chapter) => (
            <div key={chapter.id} className="nav-item">
              <a 
                href={`#${chapter.id}`}
                className={`nav-link ${currentChapter.id === chapter.id ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  setCurrentChapter(chapter);
                  setIsSidebarOpen(false);
                }}
              >
                <span className="nav-number">{chapter.id}</span>
                <span>{chapter.title}</span>
                <ChevronRight size={14} style={{ marginLeft: 'auto', opacity: 0.5 }} />
              </a>
            </div>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header-actions">
          <button className="icon-btn" onClick={toggleTheme} title="切換主題">
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          <button className="icon-btn" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} title="回到頂部">
            <ArrowUp size={20} />
          </button>
        </header>

        <div className="reader">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentChapter.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
            >
              <div style={{ marginBottom: '3rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--secondary-color)', marginBottom: '1rem', fontWeight: 600 }}>
                  <Bookmark size={20} />
                  <span>CHAPTER {currentChapter.id}</span>
                </div>
                <h1 style={{ fontSize: '3.5rem', marginBottom: '2rem' }}>{currentChapter.title}</h1>
              </div>

              {blocks.map((block, index) => (
                <motion.section 
                  key={index}
                  className="content-card"
                  initial={{ opacity: 0, scale: 0.95 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true, margin: "-100px" }}
                  transition={{ delay: index * 0.1 }}
                  style={{ marginBottom: '2rem' }}
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {block}
                  </ReactMarkdown>
                </motion.section>
              ))}
            </motion.div>
          </AnimatePresence>
        </div>

        <footer style={{ marginTop: '4rem', padding: '2rem 0', borderTop: '1px solid var(--border-color)', textAlign: 'center', color: 'var(--text-muted)' }}>
          <p>© 2026 iPAS 品牌企劃師：數位辭典型課本 | 高感度模組化學習體驗</p>
        </footer>
      </main>
    </>
  );
}

export default App;
