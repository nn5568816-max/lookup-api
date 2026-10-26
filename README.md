VERCEL LOOKUP API - DEPLOYMENT

1. Extract this ZIP.
2. In VS Code, open the extracted lookup-api-fixed folder itself.
3. Ensure vercel.json and api/ are directly inside that folder.
4. Install Vercel CLI if needed:
     npm install -g vercel
5. In the VS Code terminal, from the project root:
     vercel
6. Test:
     https://YOUR-DEPLOYMENT.vercel.app/api/
     https://YOUR-DEPLOYMENT.vercel.app/api/ifsc?ifsc=SBIN0000001
     https://YOUR-DEPLOYMENT.vercel.app/api/aadhaar?id=234567890124
     https://YOUR-DEPLOYMENT.vercel.app/api/vehicle?registration=HR55AL0051
7. Deploy production:
     vercel --prod

IFSC:
Defaults to the user's supplied HTTPS endpoint. You may override it with the
Vercel environment variable IFSC_API_TEMPLATE, containing {ifsc}.

AADHAAR:
This endpoint only validates the 12-digit format and returns a masked value.
It does not verify identity or call an identity lookup service.

VEHICLE:
Requires an authorized provider. Set VEHICLE_API_TEMPLATE to its documented
HTTPS endpoint containing {registration}, and set VEHICLE_API_KEY to a real
key in Vercel Project Settings > Environment Variables. Do not use demo keys
for personal data lookups.

Note: This project does not require a custom "python" runtime declaration.
