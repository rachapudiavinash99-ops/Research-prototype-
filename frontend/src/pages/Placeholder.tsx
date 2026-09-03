import React from 'react';
export default function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-gray-500">
      <h2 className="text-2xl font-bold mb-2">{title}</h2>
      <p>This module is currently under active development.</p>
    </div>
  );
}
