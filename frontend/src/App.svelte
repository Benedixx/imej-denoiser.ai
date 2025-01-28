<script>
  let selectedFile = null;
  let originalImage = null;
  let denoisedImage = null;
  let isProcessing = false;

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    selectedFile = file;
    originalImage = URL.createObjectURL(file);
    denoisedImage = "";
  }

  const handleDenoise = async () => {
    if (!selectedFile) {
      alert("Euy, pilih dulu gambarnya!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      isProcessing = true;
      const res = await fetch("http://localhost:8000/denoise", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to denoise the image");
      }

      const blob = await res.blob();
      denoisedImage = URL.createObjectURL(blob);
    }
    catch (err) {
      console.error(err);
      alert("Gagal memproses gambar");
    }
    finally {
      isProcessing = false;
    }
  }

</script>

<main>
  <h1>imej denoiser</h1>
  <div class="image-container">
    <!-- Gambar Original -->
    {#if originalImage}
      <img src={originalImage} alt="" class="image" />
    {/if}

    <!-- Tombol Denoise -->
    <div class="controls">
      <input type="file" accept="image/*" on:change={handleFileUpload} />
      <button on:click={handleDenoise} disabled={isProcessing}>
        {isProcessing ? "Processing..." : "Denoise"}
      </button>
    </div>

    <!-- Gambar Denoise -->
    {#if denoisedImage}
      <img src={denoisedImage} alt="" class="image" />
    {/if}
  </div>
</main>

<style>
  main {
    text-align: center;
    margin: 20px auto;
    max-width: 800px;
  }

  .image-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
  }

  .controls {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .image {
    max-width: 300px;
    max-height: 300px;
    object-fit: cover;
    border: 2px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }

  button {
    padding: 10px 20px;
    border: none;
    background-color: #007bff;
    color: #fff;
    font-size: 16px;
    border-radius: 5px;
    cursor: pointer;
  }

  button:disabled {
    background-color: #aaa;
    cursor: not-allowed;
  }

  input[type="file"] {
    margin-bottom: 10px;
  }
</style>