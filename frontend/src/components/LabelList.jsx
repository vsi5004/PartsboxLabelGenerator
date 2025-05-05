import React from 'react';
import Label from './Label';

const LabelList = ({ labels }) => (
  <div className="label-preview">
    {labels.map((label, idx) => (
      <Label key={idx} url={label.url} location={label.location} />
    ))}
  </div>
);

export default LabelList;
