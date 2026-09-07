# NORTHPOINT

En liten grund för en webbshop, utan produktinnehåll eller extra sidor.

- `frontend/pencil-webbshop`: Vue 3, Vite, Vuetify och Pinia.
- `backend`: FastAPI och SQLite.

## Starta backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Starta frontend

```powershell
cd frontend/pencil-webbshop
Copy-Item .env.example .env
npm install
npm run dev
```

Frontendens API-adress konfigureras med `VITE_API_BASE_URL` i `.env`.

Så fungerar webbshop-projektet

1. Översikt

Projektet är en webbshop uppdelad i tre tydliga delar:

Frontend: Vue 3, TypeScript, Vite, Vuetify, Vue Router och
Pinia.

Backend: FastAPI, Pydantic, SQLAlchemy och Alembic.

Databas: SQLite under utveckling.

Grundflödet är:

Användare
   ↓
Vue-komponent / View
   ↓
Pinia Store (när gemensamt state behövs)
   ↓
Service
   ↓
client.ts
   ↓ HTTP/JSON
FastAPI Route
   ↓
Service
   ↓
Repository
   ↓
SQLAlchemy
   ↓
SQLite

Varje lager har ett eget ansvar. Vue ansvarar för gränssnittet, FastAPI
ansvarar för regler, validering och behörighet, och SQLite lagrar
informationen.

2. Frontend

Frontend är det användaren ser och interagerar med i webbläsaren.

En möjlig struktur är:

frontend/
└── src/
    ├── components/
    ├── views/
    ├── services/
    │   ├── client.ts
    │   ├── productService.ts
    │   ├── authService.ts
    │   └── orderService.ts
    ├── stores/
    │   ├── productStore.ts
    │   ├── authStore.ts
    │   └── cartStore.ts
    ├── router/
    ├── types/
    ├── App.vue
    └── main.ts

Den viktigaste principen är att komponenterna inte själva ska behöva
känna till alla detaljer om API-anrop.

3. Vue-komponenter och Views

Komponenterna bygger själva användargränssnittet.

Exempel:

ProductView.vue
ProductCard.vue
CartView.vue
LoginView.vue
AdminProductView.vue

En komponent ska främst ansvara för:

presentation

användarinteraktion

formulär

knappar

laddningsindikatorer

felmeddelanden

En komponent bör inte innehålla all logik för hur HTTP-anrop fungerar.

Exempelvis ska ProductView.vue inte behöva veta exakt hur URL till
FastAPI byggs eller hur Authorization-headern sätts.

Istället använder komponenten en Store eller Service.

4. Pinia Store

Pinia används för state som behöver delas eller leva kvar mellan flera
komponenter.

Exempel:

ProductView
ProductCard
Navbar
CartView

kan behöva information som hanteras centralt.

En Store kan exempelvis innehålla:

State
├── products
├── loading
└── error

Actions
├── fetchProducts()
├── createProduct()
└── updateProduct()

Komponenten kan då göra något i stil med:

ProductView
    ↓
productStore.fetchProducts()

Store anropar sedan rätt service:

productStore
    ↓
productService.getProducts()

När resultatet kommer tillbaka sparas det i Store:n:

FastAPI
   ↓
productService
   ↓
productStore.products
   ↓
ProductView

Vue reagerar automatiskt när Store förändras och uppdaterar
gränssnittet.

När behövs Pinia?

Pinia ska inte användas bara för att det finns.

Det passar bra för exempelvis:

inloggad användare

autentiseringsstatus

kundvagn

produkter som delas mellan flera komponenter

global applikationsstatus

Om data bara behövs i en enda komponent kan komponenten ibland anropa en
service direkt.

5. Service-lagret

Services beskriver vad frontend vill göra mot backend.

Exempel:

services/
├── client.ts
├── productService.ts
├── authService.ts
└── orderService.ts

productService.ts kan exempelvis erbjuda funktioner för:

getProducts()
getProduct(id)
createProduct(data)
updateProduct(id, data)
deleteProduct(id)

Service-lagret känner till webbshopens API-endpoints, men bör inte
behöva upprepa den grundläggande HTTP-konfigurationen.

Där kommer client.ts in.

6. client.ts

client.ts är den gemensamma ingången till backend.

Istället för att varje service själv konfigurerar HTTP-anrop används
samma klient.

productService ──┐
authService ─────┼──→ client.ts ──→ FastAPI
orderService ────┤
userService ─────┘

client.ts kan exempelvis ansvara för:

backendens base URL

gemensamma headers

JSON-hantering

autentisering/JWT

gemensam felhantering

Exempel på princip:

VITE_API_URL=http://localhost:8000

client.ts använder den konfigurationen och services behöver därför
inte hårdkoda:

http://localhost:8000

överallt.

Det gör det också enklare att senare byta från lokal backend till en
produktionsserver.

7. Hela frontend-flödet

Anta att användaren öppnar produktsidan.

Steg 1 -- komponenten

ProductView.vue

behöver produkter.

Den anropar:

productStore.fetchProducts()

Steg 2 -- Store

productStore hanterar state och anropar:

productService.getProducts()

Steg 3 -- Service

productService vet att produkterna finns på exempelvis:

GET /api/products

och använder client.ts.

Steg 4 -- Client

client.ts skapar HTTP-anropet:

GET http://localhost:8000/api/products

Steg 5 -- Backend

FastAPI tar emot anropet och hämtar produkterna.

Steg 6 -- Svaret

Svaret går tillbaka samma väg:

SQLite
   ↓
FastAPI
   ↓ JSON
client.ts
   ↓
productService
   ↓
productStore
   ↓
ProductView.vue
   ↓
Användaren ser produkterna

Det är kärnan i kommunikationen mellan frontend och backend.

8. Backend

Backend körs med FastAPI.

En tydlig struktur är:

backend/
└── app/
    ├── api/
    │   └── routes/
    ├── models/
    ├── schemas/
    ├── repositories/
    ├── services/
    ├── core/
    ├── db/
    └── main.py

Backendens huvudsakliga flöde är:

Route
   ↓
Service
   ↓
Repository
   ↓
Database

Det motsvarar ungefär frontends uppdelning i komponent, Store, Service
och Client.

9. FastAPI Route

En Route är ingången till backend.

Exempel:

GET    /api/products
GET    /api/products/{id}
POST   /api/admin/products
PATCH  /api/admin/products/{id}
DELETE /api/admin/products/{id}

Route-lagret ansvarar bland annat för:

vilken URL som används

HTTP-metod

inkommande data

dependencies

autentisering

behörighetskontroll

HTTP-statuskoder

Route-filen bör däremot inte innehålla stora mängder affärslogik.

10. Pydantic Schemas

Data från frontend ska inte skickas direkt till databasen.

Pydantic används som gräns mellan API och resten av backend.

Exempel:

ProductCreate
ProductUpdate
ProductResponse

Ett ProductCreate kan kontrollera exempelvis:

att namn finns

maximal längd

att pris är positivt

att rätt datatyper används

Flödet blir:

Frontend JSON
      ↓
FastAPI
      ↓
Pydantic
      ↓
Validerad Python-data

Frontendens TypeScript-typer är bra för utveckling och
användarupplevelse, men backend måste alltid validera informationen
igen.

11. Service-lagret i backend

Backendens Service innehåller affärslogiken.

Det är här systemet bestämmer vad som faktiskt får ske.

Exempel för en order:

Order Route
    ↓
Order Service

Order Service kan exempelvis:

kontrollera produkterna

kontrollera antal

hämta priser från databasen

beräkna totalsumman

skapa ordern

Frontend ska alltså inte få bestämma det slutliga priset.

Frontend kan skicka:

{
  "product_id": 10,
  "quantity": 2
}

Backend hämtar själv produktens riktiga pris.

12. Repository

Repository är lagret som kommunicerar med databasen.

Exempel:

ProductService
      ↓
ProductRepository
      ↓
SQLAlchemy
      ↓
SQLite

Repository kan innehålla operationer som:

find_all()
find_by_id()
create()
update()
delete()

Fördelen är att Service inte behöver känna till detaljerna kring
SQLAlchemy.

13. SQLAlchemy Models

SQLAlchemy-modeller beskriver hur informationen lagras i databasen.

Exempel på en produkt kan innehålla:

Product
├── id
├── name
├── slug
├── description
├── price
├── currency
├── active
├── stock
├── created_at
└── updated_at

Det är viktigt att skilja på:

Pydantic Schema ≠ SQLAlchemy Model

Pydantic beskriver vad API tar emot och skickar.

SQLAlchemy Model beskriver hur data lagras i databasen.

14. SQLite

SQLite är själva databasen under utvecklingen.

Den kan exempelvis ligga som:

backend/webshop.db

SQLAlchemy ligger mellan applikationen och SQLite:

FastAPI
   ↓
Service
   ↓
Repository
   ↓
SQLAlchemy
   ↓
SQLite

Det betyder att resten av applikationen inte behöver byggas direkt runt
SQLite.

Det gör det enklare att senare byta till exempelvis PostgreSQL.

15. Alembic

Alembic används för databasmigreringar.

När databasstrukturen förändras bör databasen inte ändras manuellt.

Exempel:

Först har Product:

id
name
price

Sen vill vi lägga till:

stock

Då skapas en migration som beskriver förändringen.

Det gör databasens utveckling spårbar och reproducerbar.

16. Autentisering och JWT

När användaren loggar in skickar frontend användarnamn och lösenord till
backend.

Principen är:

LoginView
   ↓
authStore
   ↓
authService
   ↓
client.ts
   ↓
POST /auth/login
   ↓
FastAPI

Backend kontrollerar användaren och det hashade lösenordet.

Vid korrekt inloggning kan backend skapa en JWT access token.

JWT representerar den autentiserade användaren under en begränsad tid.

Vid ett skyddat API-anrop blir principen:

Vue
 ↓
client.ts
 ↓
Authorization: Bearer <JWT>
 ↓
FastAPI
 ↓
Verifiera JWT
 ↓
Identifiera användaren
 ↓
Kontrollera behörighet

Det är viktigt att frontendens rollkontroller inte betraktas som
säkerhet.

Vue Router kan exempelvis förhindra att en vanlig användare enkelt går
till:

/admin/products

men användaren kan fortfarande försöka anropa backend manuellt.

Därför måste FastAPI också kontrollera rollen.

Frontend:
"Du ska inte se admin-sidan."

Backend:
"Du får inte utföra admin-operationen."

Backend är den slutliga auktoriteten.

17. Exempel: admin skapar en produkt

Ett komplett flöde kan se ut så här:

AdminProductView.vue
        ↓
productStore.createProduct()
        ↓
productService.createProduct()
        ↓
client.ts
        ↓
POST /api/admin/products
Authorization: Bearer <JWT>
        ↓
FastAPI Route
        ↓
Kontrollera JWT
        ↓
Kontrollera ADMIN-roll
        ↓
ProductCreate
Pydantic-validering
        ↓
ProductService
        ↓
ProductRepository
        ↓
SQLAlchemy
        ↓
SQLite

Svaret går sedan tillbaka:

SQLite
   ↓
Repository
   ↓
Service
   ↓
Route
   ↓ JSON
client.ts
   ↓
productService
   ↓
productStore
   ↓
AdminProductView

18. Vue Router

Vue Router bestämmer vilken View som ska visas för en viss URL.

Exempel:

/                 → HomeView
/shop             → ShopView
/products         → ProductView
/cart             → CartView
/checkout         → CheckoutView
/faq              → FaqView
/about            → AboutView
/account          → AccountView
/admin/products   → AdminProductView

Router guards kan användas för att styra gränssnittet utifrån om
användaren är inloggad och vilken roll användaren har.

Det ersätter dock aldrig backendens authorization.

19. Vuetify

Vuetify används för själva gränssnittet.

Exempel:

v-app
v-app-bar
v-navigation-drawer
v-card
v-btn
v-text-field
v-dialog
v-data-table

Vuetify ansvarar alltså inte för data eller API-kommunikation.

Principen är:

Vuetify
= hur det ser ut

Vue Component
= hur UI:t beter sig

Pinia
= gemensamt state

Service
= vad vi vill göra mot API:t

client.ts
= hur vi kommunicerar med API:t

20. i18n och språk

Frontend är förberedd för flera språk.

Planerade språk är:

svenska

engelska

tyska

Texter i gränssnittet bör därför inte hårdkodas överallt.

Istället kan översättningsnycklar användas så att samma komponent kan
visas på olika språk.

Språkvalet påverkar främst presentationen i Vue och ska hållas separat
från backendens säkerhet och affärslogik.

21. Säkerhetsprincipen

Den viktigaste säkerhetsprincipen i projektet är:

Frontend är aldrig den slutliga auktoriteten.

En användare kan manipulera JavaScript, API-anrop och formulär.

Därför måste backend kontrollera exempelvis:

Behörighet
Priser
Antal
Produkt-ID
Orderstatus
Användar-ID
Inkommande data

Ett exempel är en order.

Frontend kanske visar:

Penna
100 kr
Antal: 2
Totalt: 200 kr

Men frontend ska inte kunna säga till backend:

total = 1 kr

Backend ska istället göra:

product_id + quantity
        ↓
Hämta produkt från databasen
        ↓
Hämta korrekt pris
        ↓
Beräkna total
        ↓
Skapa order

22. Lokal utveckling

Under utveckling körs frontend och backend separat.

Frontend

cd frontend
npm run dev

Normalt:

http://localhost:5173

Backend

cd backend
uvicorn app.main:app --reload

Normalt:

http://localhost:8000

Frontend kommunicerar sedan med backend över HTTP.

23. Bygga frontend

När projektet ska visas i ett mer produktionslikt läge kan frontend
byggas:

npm run build

Vite skapar då normalt:

frontend/dist/

Den byggda versionen kan testas lokalt med:

npm run preview

Vanligtvis blir flödet:

Webbläsare
http://localhost:4173
        ↓
Byggd Vue-app
        ↓
FastAPI
http://localhost:8000
        ↓
SQLite

Under vanlig utveckling används däremot npm run dev, eftersom Vite då
automatiskt uppdaterar applikationen när koden ändras.

24. Sammanfattning

Hela systemet kan förenklas till två huvudsakliga kedjor.

Frontend

Vue Component
      ↓
Pinia Store
      ↓
Service
      ↓
client.ts
      ↓
HTTP

Pinia används endast när state faktiskt behöver delas eller hanteras
centralt. En enkel komponent kan i vissa fall använda en service direkt.

Backend

FastAPI Route
      ↓
Pydantic-validering
      ↓
Service
      ↓
Repository
      ↓
SQLAlchemy
      ↓
SQLite

Och tillsammans:

┌──────────────── FRONTEND ────────────────┐

Vue Component
      ↓
Pinia Store
      ↓
Service
      ↓
client.ts

└───────────────────┬──────────────────────┘
                    │
                 HTTP/JSON
                    │
┌───────────────────▼──────────────────────┐

FastAPI Route
      ↓
Pydantic
      ↓
Service
      ↓
Repository
      ↓
SQLAlchemy
      ↓
SQLite

└──────────────── BACKEND ─────────────────┘

Det ger en tydlig ansvarsfördelning: komponenterna visar information,
Pinia hanterar delat state, services beskriver API-operationer,
client.ts sköter den gemensamma HTTP-kommunikationen, FastAPI tar emot
och validerar anrop, backend-services hanterar regler, repositories
arbetar mot databasen och SQLAlchemy kommunicerar med SQLite.
