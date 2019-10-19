const fs = require("fs");

// check if the directory to be created already exists?
if( fs.existsSync("storage-files")) {
    console.log("Directory already exists");
} else {
    // to create a directory...
    fs.mkdir("storage-files", err => {
        if ( err ) {
            throw err;
        }
    
        console.log("Directory created");
    });
}
