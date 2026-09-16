from django.core.management.base import BaseCommand
from webapp.models import Review  # ganti jika modelnya beda
from serpapi import GoogleSearch
import time

# class Command(BaseCommand):
#     help = 'Ambil review dari Google Maps dan simpan ke database'

#     def handle(self, *args, **kwargs):
#         params = {
#             "engine": "google_maps_reviews",
#             "data_id": "0x2e7881a84f19c03b:0x87990377e6ee814b",
#             "api_key": "d324c81daaa4b9761f9549eefefab840a56493830aefbef25793fd8525b3c846"
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()

#         for r in results.get("reviews", []):
#             Review.objects.get_or_create(
#                 name=r["user"]["name"],
#                 rating=r["rating"],
#                 content=r["snippet"]
#             )

#         self.stdout.write(self.style.SUCCESS('Review berhasil dimasukkan ke DB!'))



















class Command(BaseCommand):
    help = 'Ambil review dari Google Maps dan simpan ke database'

    def handle(self, *args, **kwargs):
        params = {
            "engine": "google_maps_reviews",
            "data_id": "0x2e7881a84f19c03b:0x87990377e6ee814b",  # Ganti dengan data_id yang sesuai
            "api_key": "d324c81daaa4b9761f9549eefefab840a56493830aefbef25793fd8525b3c846"  # Ganti dengan api_key yang sesuai
        }

        # Membuat objek pencarian
        search = GoogleSearch(params)

        # Menangani pagination untuk mendapatkan semua review
        all_reviews = []
        page = 1
        max_reviews = 40  # Membatasi jumlah review yang diambil sesuai dengan jumlah review yang ada di halaman

        while True:
            self.stdout.write(self.style.NOTICE(f"Memuat halaman {page}..."))
            params['page'] = page  # Menambahkan nomor halaman untuk pagination
            search = GoogleSearch(params)
            results = search.get_dict()

            # Cek jika hasilnya kosong atau sudah mencapai akhir
            reviews = results.get("reviews", [])
            if not reviews:
                self.stdout.write(self.style.WARNING("Tidak ada review pada halaman ini atau API tidak mengembalikan data yang valid. Menghentikan pengambilan data."))
                break  # Berhenti jika tidak ada lagi review

            # Tambahkan hanya review yang belum diambil
            all_reviews.extend(reviews)

            # Jika sudah mencapai jumlah review yang diinginkan, hentikan proses
            if len(all_reviews) >= max_reviews:
                break

            page += 1
            time.sleep(2)

        # Menyimpan review ke database
        self.stdout.write(self.style.SUCCESS(f"Total {len(all_reviews)} review ditemukan. Menyimpan ke database..."))
        for r in all_reviews[:max_reviews]:  # Simpan hanya sampai jumlah maksimum yang diinginkan
            Review.objects.get_or_create(
                name=r["user"]["name"],
                rating=r["rating"],
                content=r["snippet"]
            )

        self.stdout.write(self.style.SUCCESS(f'{len(all_reviews)} review berhasil dimasukkan ke DB!'))