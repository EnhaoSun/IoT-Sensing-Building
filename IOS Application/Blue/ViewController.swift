//
//  ViewController.swift
//  Blue
//
//  Created by 孙恩浩 on 24/12/2017.
//  Copyright © 2017 孙恩浩. All rights reserved.
//

import Foundation
import UIKit
import CoreBluetooth

var BLEPeripheral : CBPeripheral?

class ViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, CBCentralManagerDelegate, CBPeripheralDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.peripherals.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // connect to device where the peripheral is connected
        let cell = tableView.dequeueReusableCell(withIdentifier:"DeviceCell") as! PeripheralTableViewCell
        let peripheral = self.peripherals[indexPath.row]
        let rssi = self.RSSIs[indexPath.row]
        
        if peripheral.name == nil{
            cell.peripheralLabel.text = "None"
        }else{
            cell.peripheralLabel.text = peripheral.name
        }
        cell.rssiLabel.text = "RSSI:  \(rssi)"

        return cell
    }
    
    // connect to selected peripherals
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        BLEPeripheral = peripherals[indexPath.row]
        connectDevice()
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 70
    }


    /*
    Perpherial Service object
    */
    
    var centralManager : CBCentralManager!
    var peripherals: [CBPeripheral] = []
    var RSSIs = [NSNumber]()
    let piServiceCBUUID = CBUUID(string: "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF0")
    var writeCharacteristic: CBCharacteristic!
    
    @IBOutlet weak var perpherialTable: UITableView!
    
    /*
    UI item
    */
    let alertController = UIAlertController(title: "Application requires Bluetooth", message: "Please enable Bluetooth to continue using this app", preferredStyle: .alert)
    let okAction = UIAlertAction(title: "OK", style: .default, handler: nil)
    
    // scan perpherial
    
    @IBAction func scanPerpherial(_ sender: UIBarButtonItem) {
        if sender.title == "Scan"{
            if centralManager.state == .poweredOn{
                sender.title = "Stop"
                self.centralManager?.scanForPeripherals(withServices: nil, options: [CBCentralManagerScanOptionAllowDuplicatesKey:false])
            }else{
                self.present(alertController, animated: true, completion: nil)
            }
        }else{
            sender.title = "Scan"
            self.centralManager?.stopScan()
        }
    }
    
    // clear table list
    @IBAction func refreshScan(_ sender: UIBarButtonItem) {
        self.peripherals = []
        self.RSSIs = []
        refreshTableView()
    }
    
    func refreshTableView(){
        perpherialTable.reloadData()
    }
    
    

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        alertController.addAction(okAction)
        centralManager = CBCentralManager(delegate: self, queue: nil)
        
        perpherialTable.dataSource = self
        perpherialTable.delegate = self
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    
    

    /*
     Invoked when the central manager's state is updated
     This is where kick off the scan if Bluetooth is turned on
    */
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        switch central.state{
            case .unknown:
                print("central.state is unknown")
            case .resetting:
                print("central.state is reseeting")
            case .unsupported:
                print("central.state is unsupported")
            case .unauthorized:
                print("central.state is unauthorized")
            case .poweredOff:
                //UI Alert
                print("Bluetooth Disabled, Make sure your Bluetooth is turned on")
            case .poweredOn:
                print("Bluetooth service Enabled")
                //start scan
        }
    }
    
    // discovered peripheral
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {

        // avoid duplicated peripheral
        if !self.peripherals.contains(peripheral){
            self.peripherals.append(peripheral)
            self.RSSIs.append(RSSI)
            self.perpherialTable.reloadData()
        }

    }
    
    // connect to device
    func connectDevice(){
        centralManager?.connect(BLEPeripheral!, options: nil)
    }
    
    // connected peripheral
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        print("Connected!")
        // once connected, move to new view controller
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let conversationViewController = storyboard.instantiateViewController(withIdentifier: "ConversationViewController") as! ConversationViewController
        conversationViewController.peripheral = peripheral
        conversationViewController.centralManager = central
        
        conversationViewController.connected = true
        conversationViewController.disconnect.title = "Disconnect"
        
        centralManager?.stopScan()
        navigationController?.pushViewController(conversationViewController, animated: true)
    }

    // connection failed
    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
        print("disconnect to peripheral")
    }
    func centralManager(_ central: CBCentralManager, didFailToConnect peripheral: CBPeripheral, error: Error?) {
        print("Failed to connect peripheral")
    }

}

