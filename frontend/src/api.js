export async function fetchLocation(url) {
    const form = new FormData();
    form.append('url', url);
  
    const response = await fetch('http://localhost:8000/get-location', {
      method: 'POST',
      body: form,
    });
  
    return await response.json();
  }
  