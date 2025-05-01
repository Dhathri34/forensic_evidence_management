pragma solidity >= 0.8.11 <= 0.8.11;

contract Crime_SmartContract{

struct filedata {
        uint timestamp;
        string data;
    }

struct requestdata {
        uint timestamp;
        string rptdata;
    }

 filedata[] public fdata;
 requestdata[] public rdata;


  //call this function to register user request data to Blockchain
    function setData(string memory r) public {
       bytes memory filebytes = bytes(r);

       filedata memory newContent = filedata({
        data:r,
        timestamp: block.timestamp
       });

    fdata.push(newContent);
    }
   //get request details
    function getData() public view returns (filedata[] memory) {
        return fdata;
    }

    //call this function to register user request data to Blockchain
    function setReport(string memory rr) public {
       bytes memory requestbytes = bytes(rr);

       requestdata memory newContent = requestdata({
        rptdata:rr,
        timestamp: block.timestamp
       });

    rdata.push(newContent);
    }
   //get request details
    function getReport() public view returns (requestdata[] memory) {
        return rdata;
    }

}
