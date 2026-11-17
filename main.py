import json
import datetime
import os

# Define the file where claims will be persistently stored.
# This simulates the "meticulous recording" aspect of the article.
DATA_FILE = "interview_claims.json"

class InterviewClaim:
    """
    Represents a single claim made during an interview or professional discussion.
    Each claim is structured with key details for meticulous record-keeping.
    """
    def __init__(self, claimant, context, claim_text, status="Pending"):
        self.claimant = claimant
        self.context = context
        self.claim_text = claim_text
        self.timestamp = datetime.datetime.now().isoformat() # Automatically record when the claim was noted
        self.status = status # Track the status of the claim (e.g., Pending, Verified, Actioned)

    def to_dict(self):
        """Converts the claim object to a dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "claimant": self.claimant,
            "context": self.context,
            "claim_text": self.claim_text,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """Creates an InterviewClaim object from a dictionary."""
        claim = InterviewClaim(
            data["claimant"],
            data["context"],
            data["claim_text"],
            data.get("status", "Pending")
        )
        claim.timestamp = data["timestamp"] # Preserve original timestamp when loading
        return claim

def load_claims():
    """Loads all recorded claims from the DATA_FILE."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [InterviewClaim.from_dict(d) for d in data]
    except json.JSONDecodeError:
        print(f"Uyarı: {DATA_FILE} dosyası bozuk veya boş. Yeni bir dosya oluşturuluyor.")
        return []

def save_claims(claims):
    """Saves the current list of claims to the DATA_FILE.
    This is the core mechanism for persistent, meticulous recording."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([c.to_dict() for c in claims], f, indent=4, ensure_ascii=False)

def add_claim(claims):
    """Prompts the user for details and adds a new claim to the list."""
    print("\nYeni Bir İddia Kaydet:")
    claimant = input("İddia Sahibi (örn: Aday Ahmet, Müşteri Ayşe): ")
    context = input("Mülakat/Toplantı Konusu (örn: Senior Dev Mülakatı, Proje X Durum Değerlendirmesi): ")
    claim_text = input("İddia Metni: ")
    
    new_claim = InterviewClaim(claimant, context, claim_text)
    claims.append(new_claim)
    save_claims(claims) # Immediately save to ensure the claim is meticulously recorded
    print("İddia başarıyla kaydedildi.")

def view_claims(claims):
    """Displays all recorded claims in a readable format."""
    if not claims:
        print("\nHenüz kaydedilmiş bir iddia bulunmamaktadır.")
        return
    
    print("\n--- Kaydedilmiş İddialar ---")
    for i, claim in enumerate(claims):
        print(f"\n{i+1}. İddia:")
        print(f"  Zaman Damgası: {claim.timestamp}")
        print(f"  İddia Sahibi: {claim.claimant}")
        print(f"  Konu: {claim.context}")
        print(f"  İddia: {claim.claim_text}")
        print(f"  Durum: {claim.status}") # Showing the current status, which can be updated

def update_claim_status(claims):
    """Allows updating the status of an existing claim, demonstrating ongoing management of records."""
    view_claims(claims)
    if not claims:
        return

    try:
        index = int(input("\nDurumunu güncellemek istediğiniz iddia numarasını girin: ")) - 1
        if 0 <= index < len(claims):
            new_status = input("Yeni durum (örn: Onaylandı, Reddedildi, Takip Edilecek): ")
            claims[index].status = new_status
            save_claims(claims) # Save changes to reflect the updated status in the meticulous record
            print("İddia durumu güncellendi.")
        else:
            print("Geçersiz iddia numarası.")
    except ValueError:
        print("Geçersiz giriş.")

def main():
    """Main function to run the interview claims management application."""
    claims = load_claims() # Load existing claims at startup
    
    while True:
        print("\n--- Mülakat İddiaları Yönetimi ---")
        print("1. Yeni İddia Kaydet")
        print("2. İddiaları Görüntüle")
        print("3. İddia Durumunu Güncelle")
        print("4. Çıkış")
        
        choice = input("Seçiminizi yapın: ")
        
        if choice == '1':
            add_claim(claims)
        elif choice == '2':
            view_claims(claims)
        elif choice == '3':
            update_claim_status(claims)
        elif choice == '4':
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
