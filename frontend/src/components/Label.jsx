import React from 'react';
import QRCode from 'react-qr-code';

const Label = ({ part }) => {
  if (!part || !part.url || !part.location) {
    return <div className="label">Invalid label data</div>;
  }

  const strippedUrl = part.url.replace(/^https?:\/\//, '');

  return (
    <div className="label">
      <div className="label-content">
        <div className="qr">
          <QRCode value={strippedUrl} size={128} />
        </div>
        <div className="location">
          <span>{part.location}</span>
        </div>
      </div>
    </div>
  );
};

export default Label;
