const express = require('express');
const _ = require('lodash');
const fs = require('fs');
const app = express();

app.use(express.json());

// 存储笔记的对象
const notes = {};

// 创建新笔记
app.post('/api/notes', (req, res) => {
    const noteId = req.body.id;
    const noteData = req.body;
    
    if (!noteId) {
        return res.status(400).json({ error: 'Missing id' });
    }

    // 使用lodash.merge，该版本存在原型链污染漏洞
    notes[noteId] = {};
    _.merge(notes[noteId], noteData);
    console.log('Note prototype:', Object.getPrototypeOf(notes[noteId]));
    console.log('Note properties:', notes[noteId]);
    res.json(notes[noteId]);
});

// 获取笔记
app.get('/api/notes/:id', (req, res) => {
    const noteId = req.params.id;
    
    if (!notes[noteId]) {
        return res.status(404).json({ error: 'Note not found' });
    }
    
    res.json(notes[noteId]);
});

// 获取flag (仅管理员可访问)
app.get('/api/flag', (req, res) => {
    const noteId = req.headers['note-id'];
    
    if (!noteId || !notes[noteId]) {
        return res.status(403).json({ error: 'Authentication required' });
    }

    if (!notes[noteId].isAdmin) {
        return res.status(403).json({ error: 'Admin access required' });
    }

    try {
        const flag = fs.readFileSync('/flag', 'utf8');
        res.json({ flag: flag.trim() });
    } catch (err) {
        res.status(500).json({ error: 'Error reading flag' });
    }
});

app.listen(8000, () => {
    console.log('Server running on port 8000');
});