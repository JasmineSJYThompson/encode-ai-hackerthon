package com.aroole.myaiagent;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.github.anastr.speedviewlib.SpeedView;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.web3j.crypto.Bip32ECKeyPair;
import org.web3j.crypto.Credentials;
import org.web3j.crypto.MnemonicUtils;
import org.web3j.crypto.RawTransaction;
import org.web3j.crypto.TransactionEncoder;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.methods.response.EthGetTransactionCount;
import org.web3j.protocol.core.methods.response.EthSendTransaction;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.gas.DefaultGasProvider;
import org.web3j.utils.Convert;
import org.web3j.utils.Numeric;

import java.io.IOException;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;


public class MainActivity extends AppCompatActivity {


    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference myRef1 = database.getReference("Users");
    DatabaseReference myRef2 = database.getReference("RiskValue");

    EditText emailEditText;
    Button btn1,btn2;
    boolean copyEnable;


    EditText editText_password, recipientAddressEditText, amountEditText;
    Button createWalletButton, btnCopy, sendEthBtn;
    TextView showAddressTxtView,idTxtViewCurBal,idTxtViewEthBal,resultTxt,hisTxt;
    String walletAddress, privateKey;
    LinearLayout linearLayout;


    //private String address = "0xYourPublicAddress"; // Replace with your wallet address
    private String apiKey = "SZCH9DWDJ7PZ1GH9S1V1ZY8ZZU3Y7XAIWV";
    private String address = "0x388C818CA8B9251b393131C08a736A67ccB19297";     //consistent user address



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
//        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
//            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
//            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
//            return insets;
//        });




        new FetchTransactionsTask().execute();


         idTxtViewCurBal = findViewById(R.id.idCurBal);
         idTxtViewEthBal = findViewById(R.id.idEthBal);

         resultTxt  = findViewById(R.id.idresultTxt);



        emailEditText = findViewById(R.id.emailEditText);
        btn1 = findViewById(R.id.btn1);
        hisTxt = findViewById(R.id.idhis);
        btn2 = findViewById(R.id.btn2);
        SpeedView speedometer = findViewById(R.id.speedView);



      //  FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference("WalletUsers");

        editText_password = findViewById(R.id.passwordEditText);
        createWalletButton = findViewById(R.id.createWalletButton);
        showAddressTxtView = findViewById(R.id.addressText_012);
        btnCopy = findViewById(R.id.id_btnCopy);
        linearLayout = findViewById(R.id.idWalletCreation);

        recipientAddressEditText = findViewById(R.id.recipientAddressEditText);
        amountEditText = findViewById(R.id.amountEditText);
        sendEthBtn = findViewById(R.id.sendTransactionButton);

        String androidId = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);


        myRef2.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {


                Integer risk_value = snapshot.getValue(Integer.class);

              //  Toast.makeText(MainActivity.this, "Value : "+risk_value, Toast.LENGTH_SHORT).show();


                speedometer.speedTo(risk_value);
                // move indicator to percent value (30%)
                //  speedometer.speedPercentTo(30);
                speedometer.setUnit("% Risk");



            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {



            }
        });



        btn2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

//                Intent intent = new Intent(MainActivity.this, EthWallet.class);
//                startActivity(intent);


            }
        });



        btn1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String emailString = emailEditText.getText().toString().trim();

                if (!emailString.isEmpty()) {
//                    myRef.setValue(emailString);

                    // Push the email as a plain string
                    myRef1.push().setValue(emailString)
                            .addOnSuccessListener(aVoid -> {
                                Toast.makeText(MainActivity.this, "You are Subscribed to Ai Agent!", Toast.LENGTH_SHORT).show();
                            })
                            .addOnFailureListener(e -> {
                                Toast.makeText(MainActivity.this, "Problem in Subscribing.", Toast.LENGTH_SHORT).show();

                            });



                }

            }
        });










        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                if (snapshot.hasChild(androidId)) {
                    linearLayout.setVisibility(View.GONE);
                    resultTxt.setVisibility(View.VISIBLE);
                    hisTxt.setVisibility(View.VISIBLE);
                    showAddressTxtView.setText((CharSequence) snapshot.child(androidId).child("WalletID").getValue());
                    privateKey = snapshot.child(androidId).child("PrivateKey").getValue(String.class);  // Fetch private key
                    System.out.println("Private Key from Firebase: " + privateKey);  // For debugging

                    String walletaddressString = (String) snapshot.child(androidId).child("WalletID").getValue();
                    walletAddress = walletaddressString.toString();
                    getWalletBalance(walletAddress);



                    copyEnable = true;
                }else{

                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });




        sendEthBtn.setOnClickListener(v -> {
            String recipientAddress = recipientAddressEditText.getText().toString();
            String amountEth = amountEditText.getText().toString();

            if (!recipientAddress.isEmpty() && !amountEth.isEmpty() && privateKey != null && !privateKey.isEmpty()) {
                if (isValidEthereumAddress(recipientAddress)) {
                    try {
                        Credentials credentials = MainActivity.WalletHelper.loadWalletFromPrivateKey(privateKey);
                        sendTransaction(credentials, recipientAddress, amountEth);
                    } catch (Exception e) {
                        e.printStackTrace();
                        Toast.makeText(MainActivity.this, "Error loading wallet: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Toast.makeText(MainActivity.this, "Invalid recipient address", Toast.LENGTH_SHORT).show();
                }
            } else {
                Toast.makeText(MainActivity.this, "Please fill in all fields correctly", Toast.LENGTH_SHORT).show();
            }
        });

        btnCopy.setOnClickListener(v -> {
            if (walletAddress != null && !walletAddress.isEmpty()) {
                ClipboardManager clipboard = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
                ClipData clip = ClipData.newPlainText("myLabel", walletAddress);
                clipboard.setPrimaryClip(clip);

                Vibrator vibrator = (Vibrator) getSystemService(VIBRATOR_SERVICE);
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    vibrator.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE));
                } else {
                    vibrator.vibrate(50);
                }

            } else {

                if (!copyEnable) {
                    Toast.makeText(MainActivity.this, "No wallet available!", Toast.LENGTH_SHORT).show();
                }
            }
        });

        createWalletButton.setOnClickListener(v -> {
            String password = editText_password.getText().toString().trim();

            if (!password.isEmpty()) {
                try {
                    // Generate random 128-bit entropy for mnemonic phrase
                    byte[] entropy = new byte[16]; // 128 bits
                    new java.security.SecureRandom().nextBytes(entropy);

                    // Generate the mnemonic phrase from the entropy
                    String mnemonic = MnemonicUtils.generateMnemonic(entropy);
                    System.out.println("Generated Mnemonic: " + mnemonic);

                    // Create the wallet with the generated mnemonic
                    Credentials credentials = MainActivity.WalletHelper.createWalletFromMnemonic(mnemonic, password);

                    // Show address using Toast
//                    runOnUiThread(() -> {
//                        Toast.makeText(MainActivity.this, "ETH Address Created: " + credentials.getAddress(), Toast.LENGTH_SHORT).show();
//                    });

                    showAddressTxtView.setText(credentials.getAddress());
                    walletAddress = credentials.getAddress();
                    privateKey = credentials.getEcKeyPair().getPrivateKey().toString(16);

                    myRef.child(androidId).child("WalletID").setValue(walletAddress);
                    myRef.child(androidId).child("PrivateKey").setValue(credentials.getEcKeyPair().getPrivateKey().toString(16));
                    myRef.child(androidId).child("PublicKey").setValue(credentials.getEcKeyPair().getPublicKey().toString(16));

                    // Log the wallet information
                    System.out.println("Address: " + credentials.getAddress());
                    System.out.println("Private Key: " + credentials.getEcKeyPair().getPrivateKey().toString(16));
                    System.out.println("Public Key: " + credentials.getEcKeyPair().getPublicKey().toString(16));

                } catch (Exception e) {
                    e.printStackTrace();
                    runOnUiThread(() -> {
                        Toast.makeText(MainActivity.this, "Error: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    });
                }
            } else {
                runOnUiThread(() -> {
                    Toast.makeText(MainActivity.this, "Password field is empty", Toast.LENGTH_SHORT).show();
                });
            }
        });








    }





    // AsyncTask to fetch transactions in the background
    private class FetchTransactionsTask extends AsyncTask<Void, Void, String> {

        @Override
        protected String doInBackground(Void... voids) {
            String urlString = "https://api.etherscan.io/api?module=account&action=tokentx" +
                    "&address=" + address +
                    "&startblock=0&endblock=99999999&page=1&offset=10&sort=desc" +
                    "&apikey=" + apiKey;

            try {
                // Create URL object
                URL url = new URL(urlString);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.connect();

                // Read response
                Scanner sc = new Scanner(url.openStream());
                StringBuilder inline = new StringBuilder();
                while (sc.hasNext()) {
                    inline.append(sc.nextLine());
                }
                sc.close();

                return inline.toString();

            } catch (IOException e) {
                e.printStackTrace();
                return null;
            }
        }





    @Override
    protected void onPostExecute(String result) {
        super.onPostExecute(result);

        if (result != null) {
            try {
                // Parse JSON response
                JSONObject data_obj = new JSONObject(result);
                JSONArray transactions = data_obj.getJSONArray("result");

                StringBuilder resultText = new StringBuilder();

                // Loop through transactions and display details
//                for (int i = 0; i < transactions.length(); i++) {
                for (int i = 0; i < 5; i++) {
                    JSONObject tx = transactions.getJSONObject(i);

                    // Transaction details
                    String blockNumber = tx.getString("blockNumber");
                    String tokenName = tx.getString("tokenName");
                    String tokenSymbol = tx.getString("tokenSymbol");
                    String from = tx.getString("from");
                    String to = tx.getString("to");
                    String value = tx.getString("value");
                    String hash = tx.getString("hash");



                 //   Toast.makeText(MainActivity.this, ""+tokenName, Toast.LENGTH_SHORT).show();

                    // Append transaction details to resultText
                   // resultText.append("Block: ").append(blockNumber).append("\n");
                    resultText.append("Token: ").append(tokenName).append(" (").append(tokenSymbol).append(")\n");
                    resultText.append("From: ").append(from).append("\n");
                    resultText.append("To: ").append(to).append("\n");
                   // resultText.append("Amount: ").append(value).append("\n");
                 //   resultText.append("Hash: ").append(hash).append("\n");
                    resultText.append("-------------------------------------------------------------\n");
                }

//                 Display the result in TextView
//                resultTextView.setText(resultText.toString());
                resultTxt.setText(resultText.toString());


            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(MainActivity.this, "Error parsing data", Toast.LENGTH_SHORT).show();
            }
        } else {
            Toast.makeText(MainActivity.this, "Error fetching data", Toast.LENGTH_SHORT).show();
           }
    }
}









    // Web3 checking wallet balance
    public void getWalletBalance(String walletAddress) {
        new Thread(() -> {
            try {
                // Connect to Ethereum network via Infura
                Web3j web3 = Web3j.build(new HttpService("https://mainnet.infura.io/v3/3df9c4ab18e846e0bcfc7cc761b513b7"));

                // Fetch the balance of the given address
                BigInteger weiBalance = web3
                        .ethGetBalance(walletAddress, DefaultBlockParameterName.LATEST)
                        .send()
                        .getBalance();

                // Convert the balance from Wei to Ether
            //    BigDecimal ethBalance = Convert.fromWei(new BigDecimal(weiBalance), Convert.Unit.ETHER);
                BigDecimal ethBalance = Convert.fromWei(new BigDecimal(weiBalance), Convert.Unit.ETHER)
                        .setScale(6, RoundingMode.HALF_UP);


              //  BigDecimal resultBal = ethBalance.multiply(new BigDecimal(1200)).setScale(2, RoundingMode.HALF_UP);


                runOnUiThread(() -> {


                    idTxtViewEthBal.setText("  &  " + ethBalance.toPlainString() + " ETH");
                    idTxtViewCurBal.setText("Wallet : £ 100"); // using payments gateways like paypal,stripe values can be changed
                });

            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    idTxtViewEthBal.setText("Balance: Error");
                    Toast.makeText(MainActivity.this, "Error fetching balance"+walletAddress, Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }






    // Method to validate Ethereum address
    public boolean isValidEthereumAddress(String address) {
        return address != null && address.length() == 42 && address.startsWith("0x");
    }

    public static class WalletHelper {

        private static final int HardenedBit = 0x80000000;

        public static Credentials loadWalletFromPrivateKey(String privateKey) {
            return Credentials.create(privateKey);
        }

        public static Credentials generateWalletFromMnemonic(String mnemonic, String password) throws Exception {
            byte[] seed = MnemonicUtils.generateSeed(mnemonic, password);
            Bip32ECKeyPair masterKeypair = Bip32ECKeyPair.generateKeyPair(seed);
            final int[] derivationPath = {44 | HardenedBit, 60 | HardenedBit, 0 | HardenedBit, 0, 0};
            Bip32ECKeyPair derivedKeyPair = Bip32ECKeyPair.deriveKeyPair(masterKeypair, derivationPath);
            return Credentials.create(derivedKeyPair);
        }

        public static Credentials createWalletFromMnemonic(String mnemonic, String password) throws Exception {
            return generateWalletFromMnemonic(mnemonic, password);
        }
    }












    public void sendTransaction(Credentials credentials, String recipientAddress, String amountEth) {
        try {
            Web3j web3 = Web3j.build(new HttpService("https://mainnet.infura.io/v3/3df9c4ab18e846e0bcfc7cc761b513b7"));
            DefaultGasProvider gasProvider = new DefaultGasProvider();

            BigDecimal amount = new BigDecimal(amountEth);
            BigInteger weiValue = Convert.toWei(amount, Convert.Unit.ETHER).toBigInteger();

            EthGetTransactionCount ethGetTransactionCount = web3.ethGetTransactionCount(
                    credentials.getAddress(), DefaultBlockParameterName.LATEST).send();
            BigInteger nonce = ethGetTransactionCount.getTransactionCount();

            RawTransaction rawTransaction = RawTransaction.createEtherTransaction(
                    nonce,
                    gasProvider.getGasPrice(),
                    gasProvider.getGasLimit(),
                    recipientAddress,
                    weiValue
            );

            byte[] signedMessage = TransactionEncoder.signMessage(rawTransaction, credentials);
            String hexValue = Numeric.toHexString(signedMessage);

            EthSendTransaction ethSendTransaction = web3.ethSendRawTransaction(hexValue).send();
            if (ethSendTransaction.hasError()) {
                System.out.println("Error: " + ethSendTransaction.getError().getMessage());
            } else {
                System.out.println("Transaction Hash: " + ethSendTransaction.getTransactionHash());
                runOnUiThread(() -> {
                    Toast.makeText(MainActivity.this, "Transaction successful!" , Toast.LENGTH_LONG).show();
                });
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }








    public class TokenTransactionFetcher {

        public void main(String[] args) throws IOException, JSONException {
            String address = "0x388C818CA8B9251b393131C08a736A67ccB19297"; // Replace with your wallet address
            String apiKey = "SZCH9DWDJ7PZ1GH9S1V1ZY8ZZU3Y7XAIWV"; // Get from etherscan.io

            String urlString = "https://api.etherscan.io/api?module=account&action=tokentx" +
                    "&address=" + address +
                    "&startblock=0&endblock=99999999&page=1&offset=10&sort=desc" +
                    "&apikey=" + apiKey;

            URL url = new URL(urlString);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.connect();

            // Read response
            Scanner sc = new Scanner(url.openStream());
            StringBuilder inline = new StringBuilder();
            while (sc.hasNext()) {
                inline.append(sc.nextLine());
            }
            sc.close();

            // Parse JSON
            JSONObject data_obj = new JSONObject(inline.toString());
            JSONArray transactions = data_obj.getJSONArray("result");

            for (int i = 0; i < transactions.length(); i++) {
                JSONObject tx = transactions.getJSONObject(i);
                System.out.println("Block: " + tx.getString("blockNumber"));
                System.out.println("Token: " + tx.getString("tokenName") + " (" + tx.getString("tokenSymbol") + ")");
                System.out.println("From: " + tx.getString("from"));
                System.out.println("To: " + tx.getString("to"));
                System.out.println("Amount: " + tx.getString("value"));
                System.out.println("Hash: " + tx.getString("hash"));
                System.out.println("------");
            }



        }
    }








}