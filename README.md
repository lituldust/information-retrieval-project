# Final Project - Information Retrieval

<h1>Deskripsi Projek</h1>
<p align="justify">
Proyek ini merupakan sebuah mini search engine yang dirancang untuk melakukan pencarian (query) pada artikel-artikel bertema kesehatan. Proses pengembangan sistem melibatkan beberapa tahap, mulai dari <b>web scraping, text processing, hingga indexing</b>, yang kemudian digunakan untuk melakukan information retrieval terhadap data yang telah dikumpulkan. Hasil akhir dari proyek ini adalah sebuah sistem information retrieval yang mampu menampilkan konten-konten relevan sesuai dengan kueri yang dimasukkan oleh pengguna.
</p>

<h1>Setup</h1>
<ol>
  <li>Clone repository</li>
  
  ```
  git clone https://github.com/lituldust/information-retrieval-project
  cd information-retrieval-project
  ```

  <li>Membuat virtual environment</li>

  ```bash
  python -m venv .venv
  .venv/scripts/activate
  atau
  source .venv/scripts/activate
  ```
  <li>Install requirements</li>

  ```bash
  pip install -r requirements.txt
  ```
</ol>

<h1>Cara Melakukan Web Scraping</h1>
<ol>
  <li>Install chromedriver sesuai dengan versi chrome pada device kalian</li>
  <ul>
    <li>Cek versi chrome: Titik tiga kanan atas -> Setelan -> Tentang chrome</li>
      <img src="https://www.guidingtech.com/wp-content/uploads/Chrome-Stable.jpg" alt="versi chrome">
    <li>Download chromedriver sesuai dengan versi chrome kalian pada <a href="https://sites.google.com/chromium.org/driver/downloads">link ini</a></li>
    <li>Unzip dan pindahkan file chromedriver.exe ke folder repository</li>
  </ul>
  <li>Buka file template.py</li>
  <li>Cari elemen/tag html yang sesuai untuk discraping dengan cara: </li>
    <ul>
      <li>Buka halaman website yang akan di-scrape</li>  
      <li>Inspect halaman dengan klik <b>Ctrl + Shift + I</b></li>
      <li>Nyalakan kursor untuk pilih elemen dengan klik <b>Ctrl + Shift + C</b></li>
      <li>Arahkan kursor ke elemenm yang akan di-scrape</li>
    </ul>
    
  <li>Ikuti petunjuk dalam menuliskan elemen/tag html di kode pada <a href="https://www.scrapingbee.com/blog/selenium-python/">link ini</a>, atau bisa cek contohnya pada contoh-kompas.py</li>
</ol>
