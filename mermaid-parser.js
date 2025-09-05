/**
 * 增强版 Mermaid 语法解析器
 * 支持将 Mermaid 代码转换为 G6 数据格式
 */

class MermaidParser {
    constructor() {
        this.nodes = new Map();
        this.edges = [];
        this.nodeCounter = 0;
    }

    /**
     * 解析 Mermaid 代码
     * @param {string} mermaidCode - Mermaid 代码
     * @returns {Object} G6 数据格式
     */
    parse(mermaidCode) {
        this.nodes.clear();
        this.edges = [];
        this.nodeCounter = 0;

        const lines = mermaidCode.split('\n').filter(line => line.trim());
        
        // 检测图表类型
        const chartType = this.detectChartType(mermaidCode);
        
        switch (chartType) {
            case 'flowchart':
            case 'graph':
                return this.parseFlowchart(lines);
            case 'sequence':
                return this.parseSequenceDiagram(lines);
            case 'gantt':
                return this.parseGanttChart(lines);
            case 'class':
                return this.parseClassDiagram(lines);
            case 'state':
                return this.parseStateDiagram(lines);
            default:
                return this.parseFlowchart(lines);
        }
    }

    /**
     * 检测图表类型
     */
    detectChartType(code) {
        if (code.includes('sequenceDiagram')) return 'sequence';
        if (code.includes('gantt')) return 'gantt';
        if (code.includes('classDiagram')) return 'class';
        if (code.includes('stateDiagram')) return 'state';
        if (code.includes('graph') || code.includes('flowchart')) return 'flowchart';
        return 'flowchart';
    }

    /**
     * 解析流程图
     */
    parseFlowchart(lines) {
        lines.forEach(line => {
            line = line.trim();
            if (this.isConnectionLine(line)) {
                this.parseConnection(line);
            }
        });

        return {
            nodes: Array.from(this.nodes.values()),
            edges: this.edges
        };
    }

    /**
     * 判断是否为连接线
     */
    isConnectionLine(line) {
        return line.includes('-->') || 
               line.includes('->') || 
               line.includes('---') || 
               line.includes('--') ||
               line.includes('==>') ||
               line.includes('==');
    }

    /**
     * 解析连接线
     */
    parseConnection(line) {
        // 支持多种连接符号
        const connectionRegex = /([A-Za-z0-9_]+)\s*(--?>?|==>?)\s*([A-Za-z0-9_]+)/;
        const match = line.match(connectionRegex);
        
        if (match) {
            const [, source, connector, target] = match;
            
            // 提取标签
            let label = '';
            if (line.includes('|')) {
                const labelMatch = line.match(/\|([^|]+)\|/);
                if (labelMatch) {
                    label = labelMatch[1].trim();
                }
            }

            // 添加节点
            this.addNode(source);
            this.addNode(target);

            // 添加边
            this.edges.push({
                source: source,
                target: target,
                label: label,
                type: this.getEdgeType(connector)
            });
        }
    }

    /**
     * 获取边的类型
     */
    getEdgeType(connector) {
        if (connector.includes('==')) return 'thick';
        if (connector.includes('--')) return 'dashed';
        return 'solid';
    }

    /**
     * 添加节点
     */
    addNode(nodeId) {
        if (!this.nodes.has(nodeId)) {
            const nodeType = this.getNodeType(nodeId);
            this.nodes.set(nodeId, {
                id: nodeId,
                label: this.cleanNodeLabel(nodeId),
                type: nodeType,
                style: this.getNodeStyle(nodeType)
            });
        }
    }

    /**
     * 获取节点类型
     */
    getNodeType(nodeId) {
        if (nodeId.includes('[') && nodeId.includes(']')) return 'rect';
        if (nodeId.includes('{') && nodeId.includes('}')) return 'diamond';
        if (nodeId.includes('(') && nodeId.includes(')')) return 'round';
        if (nodeId.includes('((') && nodeId.includes('))')) return 'stadium';
        if (nodeId.includes('>') && nodeId.includes('<')) return 'rhombus';
        return 'circle';
    }

    /**
     * 清理节点标签
     */
    cleanNodeLabel(nodeId) {
        return nodeId.replace(/[\[\]{}()<>]/g, '').trim();
    }

    /**
     * 获取节点样式
     */
    getNodeStyle(nodeType) {
        const styles = {
            rect: { fill: '#DEE9FF', stroke: '#5B8FF9' },
            diamond: { fill: '#FFF2E8', stroke: '#FF7A00' },
            round: { fill: '#F6FFED', stroke: '#52C41A' },
            stadium: { fill: '#FFF1F0', stroke: '#FF4D4F' },
            rhombus: { fill: '#F9F0FF', stroke: '#722ED1' },
            circle: { fill: '#E6F7FF', stroke: '#1890FF' }
        };
        return styles[nodeType] || styles.circle;
    }

    /**
     * 解析时序图
     */
    parseSequenceDiagram(lines) {
        const participants = new Map();
        const messages = [];
        let participantY = 0;

        lines.forEach(line => {
            line = line.trim();
            
            // 解析参与者
            if (line.startsWith('participant')) {
                const match = line.match(/participant\s+(\w+)(?:\s+as\s+(\w+))?/);
                if (match) {
                    const [, id, alias] = match;
                    const name = alias || id;
                    participants.set(id, {
                        id: id,
                        label: name,
                        x: participantY * 150 + 100,
                        y: 50
                    });
                    participantY++;
                }
            }
            
            // 解析消息
            else if (line.includes('->') || line.includes('-->')) {
                const match = line.match(/(\w+)\s*(--?>)\s*(\w+):\s*(.+)/);
                if (match) {
                    const [, source, arrow, target, message] = match;
                    messages.push({
                        source: source,
                        target: target,
                        label: message,
                        type: arrow.includes('--') ? 'dashed' : 'solid'
                    });
                }
            }
        });

        // 转换为G6格式
        const nodes = Array.from(participants.values());
        const edges = messages.map((msg, index) => ({
            source: msg.source,
            target: msg.target,
            label: msg.label,
            type: msg.type,
            y: 100 + index * 50
        }));

        return { nodes, edges };
    }

    /**
     * 解析甘特图
     */
    parseGanttChart(lines) {
        const tasks = [];
        let currentSection = '';
        
        lines.forEach(line => {
            line = line.trim();
            
            if (line.startsWith('section')) {
                currentSection = line.replace('section', '').trim();
            }
            else if (line.includes(':')) {
                const match = line.match(/^(.+?)\s*:\s*(done|active|crit)?\s*,\s*(\w+)(?:,\s*(.+))?/);
                if (match) {
                    const [, name, status, id, dates] = match;
                    tasks.push({
                        id: id,
                        label: name,
                        section: currentSection,
                        status: status || 'pending',
                        dates: dates || ''
                    });
                }
            }
        });

        // 转换为G6格式（简化为节点和边）
        const nodes = tasks.map((task, index) => ({
            id: task.id,
            label: task.label,
            type: 'rect',
            x: 100,
            y: 50 + index * 60,
            style: this.getGanttNodeStyle(task.status)
        }));

        const edges = [];
        for (let i = 0; i < tasks.length - 1; i++) {
            edges.push({
                source: tasks[i].id,
                target: tasks[i + 1].id,
                type: 'dashed'
            });
        }

        return { nodes, edges };
    }

    /**
     * 获取甘特图节点样式
     */
    getGanttNodeStyle(status) {
        const styles = {
            done: { fill: '#52C41A', stroke: '#389E0D' },
            active: { fill: '#1890FF', stroke: '#096DD9' },
            crit: { fill: '#FF4D4F', stroke: '#CF1322' },
            pending: { fill: '#D9D9D9', stroke: '#8C8C8C' }
        };
        return styles[status] || styles.pending;
    }

    /**
     * 解析类图
     */
    parseClassDiagram(lines) {
        const classes = new Map();
        const relationships = [];

        lines.forEach(line => {
            line = line.trim();
            
            if (line.startsWith('class')) {
                const match = line.match(/class\s+(\w+)/);
                if (match) {
                    const className = match[1];
                    classes.set(className, {
                        id: className,
                        label: className,
                        type: 'rect',
                        methods: [],
                        properties: []
                    });
                }
            }
            else if (line.includes('+') || line.includes('-') || line.includes('#')) {
                // 解析类成员
                const match = line.match(/^(\s*)([+\-#])(.+)/);
                if (match) {
                    const [, indent, visibility, member] = match;
                    // 这里可以进一步解析类成员，暂时简化处理
                }
            }
            else if (line.includes('<|--') || line.includes('-->')) {
                // 解析关系
                const match = line.match(/(\w+)\s*(<\|--|-->)\s*(\w+)/);
                if (match) {
                    const [, source, relation, target] = match;
                    relationships.push({
                        source: source,
                        target: target,
                        type: relation === '<|--' ? 'inheritance' : 'association'
                    });
                }
            }
        });

        const nodes = Array.from(classes.values());
        const edges = relationships.map(rel => ({
            source: rel.source,
            target: rel.target,
            type: rel.type === 'inheritance' ? 'dashed' : 'solid',
            style: rel.type === 'inheritance' ? { endArrow: 'triangle' } : {}
        }));

        return { nodes, edges };
    }

    /**
     * 解析状态图
     */
    parseStateDiagram(lines) {
        const states = new Map();
        const transitions = [];

        lines.forEach(line => {
            line = line.trim();
            
            if (line.includes('-->')) {
                const match = line.match(/(\w+)\s*-->\s*(\w+)(?:\s*:\s*(.+))?/);
                if (match) {
                    const [, source, target, label] = match;
                    
                    if (!states.has(source)) {
                        states.set(source, {
                            id: source,
                            label: source,
                            type: source === '[*]' ? 'start' : 'circle'
                        });
                    }
                    
                    if (!states.has(target)) {
                        states.set(target, {
                            id: target,
                            label: target,
                            type: target === '[*]' ? 'end' : 'circle'
                        });
                    }
                    
                    transitions.push({
                        source: source,
                        target: target,
                        label: label || ''
                    });
                }
            }
        });

        const nodes = Array.from(states.values());
        const edges = transitions.map(trans => ({
            source: trans.source,
            target: trans.target,
            label: trans.label
        }));

        return { nodes, edges };
    }
}

// 导出解析器
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MermaidParser;
} else {
    window.MermaidParser = MermaidParser;
}