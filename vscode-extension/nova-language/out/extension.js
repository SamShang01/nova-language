"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
// 激活扩展
function activate(context) {
    console.log('Nova Language extension activated');
    // 注册命令
    let disposable = vscode.commands.registerCommand('nova-language.helloWorld', () => {
        vscode.window.showInformationMessage('Hello from Nova Language extension!');
    });
    // 注册运行命令
    let runDisposable = vscode.commands.registerCommand('nova-language.run', () => {
        runNovaCode();
    });
    // 注册格式化命令
    let formatDisposable = vscode.commands.registerCommand('nova-language.format', () => {
        formatNovaCode();
    });
    context.subscriptions.push(disposable);
    context.subscriptions.push(runDisposable);
    context.subscriptions.push(formatDisposable);
    // 注册文档格式化器
    vscode.languages.registerDocumentFormattingEditProvider('nova', {
        provideDocumentFormattingEdits(document) {
            return formatDocument(document);
        }
    });
}
exports.activate = activate;
// 停用扩展
function deactivate() {
    console.log('Nova Language extension deactivated');
}
exports.deactivate = deactivate;
// 运行Nova代码
function runNovaCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }
    const document = editor.document;
    if (document.languageId !== 'nova') {
        vscode.window.showErrorMessage('Active file is not a Nova file');
        return;
    }
    const content = document.getText();
    if (!content) {
        vscode.window.showWarningMessage('No code to run');
        return;
    }
    // 保存临时文件
    const fs = require('fs');
    const path = require('path');
    const os = require('os');
    const tempDir = os.tmpdir();
    const tempFile = path.join(tempDir, `temp_${Date.now()}.nova`);
    fs.writeFileSync(tempFile, content);
    // 运行Nova代码
    const { exec } = require('child_process');
    exec(`nova ${tempFile}`, (error, stdout, stderr) => {
        if (error) {
            vscode.window.showErrorMessage(`Error running Nova code: ${stderr || error.message}`);
        }
        else {
            vscode.window.showInformationMessage(`Nova code executed successfully:\n${stdout}`);
        }
        // 清理临时文件
        try {
            fs.unlinkSync(tempFile);
        }
        catch (e) {
            // 忽略清理错误
        }
    });
}
// 格式化Nova代码
function formatNovaCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }
    const document = editor.document;
    if (document.languageId !== 'nova') {
        vscode.window.showErrorMessage('Active file is not a Nova file');
        return;
    }
    const edits = formatDocument(document);
    if (edits.length > 0) {
        editor.edit(editBuilder => {
            edits.forEach(edit => editBuilder.replace(edit.range, edit.newText));
        });
    }
}
// 格式化文档
function formatDocument(document) {
    const edits = [];
    const lines = document.getText().split('\n');
    let newContent = '';
    let indentLevel = 0;
    const indentSize = 4;
    for (const line of lines) {
        const trimmedLine = line.trim();
        // 减少缩进级别
        if (trimmedLine.startsWith('}') || trimmedLine.startsWith(')') || trimmedLine.startsWith(']')) {
            indentLevel = Math.max(0, indentLevel - 1);
        }
        // 添加缩进
        const indent = ' '.repeat(indentLevel * indentSize);
        newContent += indent + trimmedLine + '\n';
        // 增加缩进级别
        if (trimmedLine.endsWith('{') || trimmedLine.endsWith('(') || trimmedLine.endsWith('[')) {
            indentLevel++;
        }
    }
    // 创建编辑
    const range = new vscode.Range(new vscode.Position(0, 0), new vscode.Position(document.lineCount, 0));
    edits.push(new vscode.TextEdit(range, newContent));
    return edits;
}
//# sourceMappingURL=extension.js.map