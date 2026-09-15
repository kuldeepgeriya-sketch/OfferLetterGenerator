# 📄 Offer Letter Generator with Google Drive Integration

A web application that generates professional offer letters and saves them to Google Drive with shareable links.

---

## 🎯 Quick Overview

This application has three main features:

1. **📋 Create Offer Letters** - Fill a form with candidate information
2. **⬇️ Download as PDF** - Get the letter on your computer
3. **☁️ Save to Google Drive** - Auto-save to cloud and get a shareable link

---

## 🚀 How to Get Started (Step-by-Step)

### **STEP 1: Get Google OAuth Credentials**

Before the app can save files to your Google Drive, you need to set up authentication. Here's how:

#### **1A: Create a Google Cloud Project**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the **project dropdown** at the top
3. Click **NEW PROJECT**
4. Enter a project name: `Offer Letter Generator`
5. Click **CREATE**
6. Wait for the project to be created (might take a minute)

#### **1B: Enable Google Drive API**

1. In the Google Cloud Console, search for **"Google Drive API"**
2. Click on **Google Drive API** from the results
3. Click the **ENABLE** button

#### **1C: Create OAuth Credentials**

1. Go to **APIs & Services** (left sidebar)
2. Click on **Credentials**
3. Click **+ CREATE CREDENTIALS** button
4. Select **OAuth client ID**
5. If prompted, click **CONFIGURE CONSENT SCREEN**
6. Select **External** and click **CREATE**
7. Fill in the form:
   - **App name**: Offer Letter Generator
   - **User support email**: Your email address
   - **Developer contact**: Your email address
   - Click **SAVE AND CONTINUE**
8. Click **SAVE AND CONTINUE** again (skip optional scopes)
9. Click **SAVE AND CONTINUE** again
10. Click **BACK TO DASHBOARD**

#### **1D: Create the Credentials File**

1. Go back to **Credentials** page
2. Click **+ CREATE CREDENTIALS** again
3. Select **OAuth client ID**
4. Choose **Desktop Application** (it's a local web app)
5. Click **CREATE**
6. Click **DOWNLOAD** button (a JSON file will download)
7. Rename the file to `credentials.json`

#### **1E: Place credentials.json in Your Project**

1. Move the downloaded `credentials.json` file to:
   ```
   C:\Users\lenovo\Desktop\OfferLetterGenerator\credentials.json
   ```

### **STEP 2: Run the Application**

Open PowerShell and run:

```powershell
cd C:\Users\lenovo\Desktop\OfferLetterGenerator
python app.py
```

You should see:
```
✅ Authenticated with Google Drive
📁 Offer Letters folder ID: xxx...
 * Running on http://localhost:5000
```

### **STEP 3: First Time Authentication**

1. Open your browser: `http://localhost:5000`
2. Click the **"Save & Share"** button
3. You'll see a Google login popup
4. Sign in with your Google account
5. Click **ALLOW** to give the app permission to access Google Drive
6. You're done! The app now has access to your Google Drive.

The app will save a token file (`token.pickle`) so you won't need to login again.

---

## 📖 How to Use the Application

### **Creating an Offer Letter:**

1. Open `http://localhost:5000` in your browser
2. Fill in all the fields:
   - **Company Information:** Your company details
   - **Candidate Information:** The person receiving the offer
   - **Employment Details:** Salary, location, dates, etc.
3. Click buttons:
   - **👁️ Preview** - See how the letter looks
   - **⬇️ Download PDF** - Save to your computer
   - **☁️ Save & Share** - Save to Google Drive and get a link

### **Sharing the Offer Letter:**

1. Click **"Save & Share"**
2. A popup will show two links:
   - **View Link** - Open the letter in browser
   - **Download Link** - Download as PDF
3. Copy the **Download Link**
4. Send it to the candidate via email
5. They can click the link to view or download the PDF

---

## 🔧 Technical Details (For Reference)

### **Project Structure:**

```
OfferLetterGenerator/
├── app.py                      # Main Flask application
├── google_drive_manager.py     # Google Drive integration
├── requirements.txt            # Python dependencies
├── credentials.json            # Google OAuth credentials (create this)
├── token.pickle                # Auto-generated after first login
│
├── templates/
│   └── index.html             # Web form
│
└── static/
    ├── style.css              # Styling
    └── script.js              # Interactivity
```

### **What Each File Does:**

| File | Purpose |
|------|---------|
| **app.py** | The backend server - receives form data, generates PDFs |
| **google_drive_manager.py** | Handles uploading files to Google Drive |
| **credentials.json** | Your Google authentication (YOU create this) |
| **token.pickle** | Auto-created - stores your login session |
| **index.html** | The web form users fill |
| **style.css** | Makes the form look professional |
| **script.js** | Makes buttons work and handles form submission |

### **How It Works (Behind the Scenes):**

```
1. User fills form in browser
2. Browser sends data to Python server
3. Server creates PDF in memory
4. PDF is sent to Google Drive
5. Google Drive creates shareable link
6. Browser shows the shareable links to user
7. User copies link and sends to candidate
8. Candidate can view/download PDF from link
```

---

## 🐛 Troubleshooting

### **"credentials.json not found" Error**

**Problem:** You see this error message
```
credentials.json not found. See setup instructions...
```

**Solution:** 
- Go back to Step 1E above
- Make sure `credentials.json` is in the correct folder:
  ```
  C:\Users\lenovo\Desktop\OfferLetterGenerator\credentials.json
  ```

### **"Application not responding" or "Connection refused"**

**Problem:** Browser shows error when going to `http://localhost:5000`

**Solution:**
- Check that Flask is running in your PowerShell
- You should see: `Running on http://localhost:5000`
- If not running, restart it: `python app.py`

### **Google Login Loop / "Redirect URI mismatch"**

**Problem:** Google login keeps failing

**Solution:**
- The app must be running on `http://localhost:5000` (not https)
- If you see "Redirect URI" error, the credentials.json might be wrong
- Delete `token.pickle` and try again

### **Files Saved to Google Drive but Can't Access**

**Problem:** Files are in Google Drive but shareable link doesn't work

**Solution:**
- Check your Google Drive: https://drive.google.com
- Accept the sharing permission if prompted
- Try opening the link in **Incognito Mode**

---

## 🔐 Security & Privacy

### **What Data is Stored?**

- **Google Drive:** Only the PDF files of offer letters
- **Your Computer:** Credentials to access your Google account (in token.pickle)
- **Cloud:** Nothing else (it's all local)

### **Can Others Access My Account?**

- The app only has permission to create and share files
- It cannot delete files or access other Google services
- Only people with the shareable link can view the letters
- You control who gets the link

---

## 📝 Customizing the Offer Letter

To change the offer letter template:

1. Open `app.py` with a text editor
2. Find the section that says `"Dear {candidate_name},..."`
3. Modify the text as needed
4. When you're ready to use a custom template, we'll add the ability to upload your own

---

## 🆘 Need Help?

Common issues and solutions:

1. **Flask not starting?** - Make sure Python is installed correctly
2. **Google login failing?** - Delete `token.pickle` and restart
3. **Links not working?** - Make sure the file is actually in Google Drive
4. **Want to customize the template?** - Let me know and I'll add that feature

---

## 📚 Next Steps

Once you've followed the setup:

1. Test the full flow with sample data
2. Share a link with someone and test if they can download
3. Once you're comfortable, provide your custom offer letter template
4. I'll update the app to use your exact template

---

## ⚡ Quick Reference

**Start the app:**
```powershell
cd C:\Users\lenovo\Desktop\OfferLetterGenerator
python app.py
```

**Access the app:**
```
http://localhost:5000
```

**View files saved:**
```
https://drive.google.com
```

**Stop the app:**
```
Press Ctrl+C in PowerShell
```

---

**Questions?** The setup is detailed but straightforward. Each step is simple - just follow them in order! ✨
