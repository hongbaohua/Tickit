import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Menu, X, Moon, Sun, Search, ArrowUp } from 'lucide-react';
import chapters from './content/index.json';

// Batch import markdown files
const markdownFiles = import.meta.glob('./content/*.md', { query: '?raw', import: 'default' });

function App() {
  const [currentChapter, setCurrentChapter] = useState(chapters[0]);
  const [content, setContent] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Load content when chapter changes
  useEffect(() => {
    const loadContent = async () => {
      const filePath = `./content/${currentChapter.file}`;
      if (markdownFiles[filePath]) {
        const mdContent = await markdownFiles[filePath]();
        setContent(mdContent as string);
        window.scrollTo(0, 0);
      }
    };
    loadContent();
  }, [currentChapter]);

  // Handle Theme Toggle
  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.setAttribute('data-theme', !isDarkMode ? 'dark' : 'light');
  };

  const filteredChapters = chapters.filter(ch => 
    ch.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      {/* Mobile Menu Button */}
      <button 
        className="icon-btn mobile-menu-btn" 
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
      >
        {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <h1 className="sidebar-title">iPAS 品牌企劃師</h1>
        
        <div style={{ position: 'relative', marginBottom: '1.5rem' }}>
          <Search size={18} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', opacity: 0.5 }} />
          <input 
            type="text" 
            placeholder="搜尋章節..." 
            style={{ width: '100%', padding: '0.6rem 0.6rem 0.6rem 2.5rem', borderRadius: '20px', border: '1px solid #ddd' }}
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
                {chapter.id}. {chapter.title}
              </a>
            </div>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="header-controls">
          <button className="icon-btn" onClick={toggleTheme}>
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          <button className="icon-btn" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <ArrowUp size={20} />
          </button>
        </div>

        <article className="reader">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </article>
      </main>
    </>
  );
}

export default App;
