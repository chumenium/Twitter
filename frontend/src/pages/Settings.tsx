import React from 'react';
import './Settings.css';

const Settings: React.FC = () => {
  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1 className="settings-title">設定</h1>
      </div>
      <div className="settings-content">
        <div className="settings-section">
          <h2>アカウント</h2>
          <ul>
            <li>メールアドレスの変更（準備中）</li>
            <li>パスワードの変更（準備中）</li>
          </ul>
        </div>
        <div className="settings-section">
          <h2>通知</h2>
          <ul>
            <li>通知設定（準備中）</li>
          </ul>
        </div>
        <div className="settings-section">
          <h2>その他</h2>
          <ul>
            <li>利用規約（準備中）</li>
            <li>プライバシーポリシー（準備中）</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Settings; 