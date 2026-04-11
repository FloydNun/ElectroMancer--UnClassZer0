import React, { useState, useRef } from 'react';
import { DataItem, DataType, ProcessingStage } from '../types';
import { saveItem, updateItem } from '../services/storageService';
import { FileText, Save, UploadCloud, Folder, LayoutGrid, Loader2, FolderOpen, Image as ImageIcon, Database, Zap, Scroll, Mic, Activity, Wand2, Terminal } from 'lucide-react';

interface MindBankProps {
  data: DataItem[];
  refreshData: () => void;
}

// DEFINING YOUR 3 LAB ZONES
const ZONES = {
  LEFT: [ 
    { name: 'IN_SMASHLAB', type: DataType.CODE, icon: <Zap size={14}/> },
    { name: 'IN_SCRIPTURES', type: DataType.IDEA, icon: <Scroll size={14}/> },
    { name: 'IN_LOGS', type: DataType.CHAT_LOG, icon: <Terminal size={14}/> },
  ],
  CENTER: [ 
    { name: 'IN_RESEARCH', type: DataType.JOURNAL, icon: <Folder size={14}/> },
    { name: 'IN_DOCS', type: DataType.JOURNAL, icon: <FileText size={14}/> },
  ],
  RIGHT: [ 
    { name: 'ARCHIVE_LAB', type: DataType.IDEA, icon: <Database size={14}/> },
    { name: 'ARTIFACTS/VISUAL', type: DataType.SCAN, icon: <ImageIcon size={14}/> },
  ]
};

export const MindBank: React.FC<MindBankProps> = ({ data, refreshData }) => {
  const [currentPath, setCurrentPath] = useState<string>('IN_RESEARCH');
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processorLog, setProcessorLog] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const currentFiles = data.filter(d => (d.folder || 'IN_DOCS') === currentPath);
  const selectedFile = data.find(d => d.id === selectedFileId);

  const handleFolderClick = (folderName: string) => { setCurrentPath(folderName); setSelectedFileId(null); };
  const handleFileClick = (file: DataItem) => { setSelectedFileId(file.id); setEditContent(file.content); };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    setIsProcessing(true);
    setProcessorLog(`Ingesting ${files.length} items...`);
    
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      let content = '';
      let type = DataType.JOURNAL;
      let targetFolder = currentPath; // Imports into whatever folder you are looking at

      if (file.type.startsWith('image/')) {
        targetFolder = 'ARTIFACTS/VISUAL'; // Auto-sort images
        const base64 = await new Promise<string>((resolve) => {
          const reader = new FileReader();
          reader.onload = (ev) => resolve(ev.target?.result as string);
          reader.readAsDataURL(file);
        });
        content = base64;
        type = DataType.SCAN;
      } else {
        content = await new Promise<string>((resolve) => {
          const reader = new FileReader();
          reader.onload = (ev) => resolve(ev.target?.result as string);
          reader.readAsText(file);
        });
      }

      const newItem: DataItem = {
        id: Math.random().toString(36).substr(2, 9),
        filename: file.name,
        type,
        content: content,
        timestamp: Date.now(),
        tags: ['raw', 'imported'],
        summary: `Imported to ${targetFolder}`,
        stage: ProcessingStage.INBOX,
        folder: targetFolder
      };
      saveItem(newItem);
    }

    refreshData();
    setIsProcessing(false);
    setTimeout(() => setProcessorLog(''), 2000);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleGenerateImage = async () => {
    if (!selectedFile) return;
    setIsProcessing(true);
    setProcessorLog('REQUESTING VISUAL SYNTHESIS...');
    // This is where we hook into the real image gen later
    await new Promise(r => setTimeout(r, 2000)); 
    setProcessorLog('IMAGE GENERATION SIMULATION COMPLETE');
    setIsProcessing(false);
    setTimeout(() => setProcessorLog(''), 2000);
  };

  const handleSaveEditor = async () => {
    if (!selectedFile) return;
    updateItem({ ...selectedFile, content: editContent });
    refreshData();
  };

  return (
    <div className="h-full flex flex-col bg-[#0d0d0d] text-gray-300 font-sans text-sm">
      {/* TOOLBAR */}
      <div className="h-10 bg-[#111] border-b border-[#222] flex items-center justify-between px-4 shrink-0">
        <div className="flex items-center gap-4">
            <span className="font-bold text-gray-400 flex items-center gap-2">
              <FolderOpen size={16} className="text-yellow-600"/> UNIFIED WORKBENCH
            </span>
            {/* IMAGE GEN BUTTON */}
            <button 
                onClick={handleGenerateImage}
                disabled={!selectedFile || isProcessing}
                className="flex items-center gap-2 px-3 py-1 bg-purple-900/30 hover:bg-purple-900/50 text-purple-400 border border-purple-800/50 rounded text-xs transition-all disabled:opacity-30"
            >
                {isProcessing ? <Loader2 size={14} className="animate-spin"/> : <Wand2 size={14}/>}
                VISUAL SYNTHESIS
            </button>
        </div>
        <div className="flex items-center gap-3">
           <span className="text-xs font-mono text-yellow-500/80 animate-pulse">{processorLog}</span>
        </div>
      </div>

      {/* 3-COLUMN LAYOUT */}
      <div className="flex-1 flex flex-row overflow-hidden">
        
        {/* LEFT: HARDWARE & SMASHLAB */}
        <div className="w-56 bg-[#050505] flex flex-col border-r border-[#222] shrink-0">
          <div className="p-3 text-[10px] font-bold text-gray-600 uppercase tracking-widest">HARDWARE LAB</div>
          <div className="flex-1 overflow-y-auto">
             {ZONES.LEFT.map(folder => (
                <div key={folder.name} onClick={() => handleFolderClick(folder.name)} className={`flex items-center gap-2 px-4 py-2 cursor-pointer ${currentPath === folder.name ? 'text-red-400 bg-[#111]' : 'text-gray-500 hover:text-gray-300'}`}>
                   {folder.icon} <span>{folder.name.replace('IN_', '')}</span>
                </div>
             ))}
          </div>
          <div className="p-3 border-t border-[#222]">
             {/* INGEST BUTTON */}
             <button onClick={() => fileInputRef.current?.click()} className="w-full flex items-center justify-center gap-2 bg-[#1a1a1a] hover:bg-[#222] text-gray-400 border border-[#333] py-2 rounded text-xs font-bold transition-all">
               <UploadCloud size={14} /> INGEST DATA
             </button>
             <input ref={fileInputRef} type="file" className="hidden" multiple onChange={handleImport} />
          </div>
        </div>

        {/* CENTER: WORK AREA */}
        <div className="flex-1 flex flex-col bg-[#000] relative border-r border-[#222]">
           {selectedFileId ? (
              <div className="flex-1 flex flex-col h-full">
                 <div className="h-10 bg-[#0a0a0a] flex items-center px-4 justify-between border-b border-[#222]">
                    <span className="text-gray-400 flex items-center gap-2"><FileText size={14}/> {selectedFile?.filename}</span>
                    <div className="flex gap-2">
                        <button onClick={handleSaveEditor} className="text-green-400 text-xs hover:bg-[#222] p-1 rounded"><Save size={14}/></button>
                        <button onClick={() => setSelectedFileId(null)} className="text-gray-400 text-xs hover:bg-[#222] p-1 rounded">CLOSE</button>
                    </div>
                 </div>
                 <textarea value={editContent} onChange={(e) => setEditContent(e.target.value)} className="flex-1 bg-[#050505] text-gray-300 p-6 font-mono resize-none focus:outline-none" />
              </div>
           ) : (
              <div className="flex-1 overflow-y-auto p-6">
                 <h2 className="text-xl font-bold text-gray-100 mb-6 flex items-center gap-2"><LayoutGrid/> {currentPath.replace('IN_', '')}</h2>
                 <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {currentFiles.map(file => (
                       <div key={file.id} onClick={() => handleFileClick(file)} className="aspect-square p-4 rounded bg-[#0a0a0a] border border-[#222] hover:border-yellow-600/50 cursor-pointer flex flex-col items-center justify-center gap-3">
                          {file.type === DataType.SCAN ? <ImageIcon size={32} className="text-purple-500"/> : <FileText size={32} className="text-gray-700"/>}
                          <span className="text-xs text-center text-gray-500 truncate w-full">{file.filename}</span>
                       </div>
                    ))}
                 </div>
              </div>
           )}
        </div>

        {/* RIGHT: DATABANK & ARCHIVE */}
        <div className="w-56 bg-[#080808] flex flex-col border-l border-[#222] shrink-0">
          <div className="p-3 text-[10px] font-bold text-gray-600 uppercase tracking-widest text-right">DATABANK</div>
          <div className="flex-1 overflow-y-auto">
             {ZONES.RIGHT.map(folder => (
                <div key={folder.name} onClick={() => handleFolderClick(folder.name)} className={`flex items-center justify-end gap-2 px-4 py-2 cursor-pointer ${currentPath === folder.name ? 'text-blue-400 bg-[#111]' : 'text-gray-500 hover:text-gray-300'}`}>
                   <span>{folder.name}</span> {folder.icon}
                </div>
             ))}
             <div className="mt-4 px-3 text-[10px] font-bold text-gray-600 uppercase tracking-widest text-right">QUICK ACCESS</div>
             {ZONES.CENTER.map(folder => (
                <div key={folder.name} onClick={() => handleFolderClick(folder.name)} className={`flex items-center justify-end gap-2 px-4 py-2 cursor-pointer ${currentPath === folder.name ? 'text-yellow-500 bg-[#111]' : 'text-gray-600 hover:text-gray-400'}`}>
                   <span>{folder.name.replace('IN_', '')}</span> {folder.icon}
                </div>
             ))}
          </div>
        </div>

      </div>
    </div>
  );
};
