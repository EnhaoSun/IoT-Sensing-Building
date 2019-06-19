//
//  PeripheralTableViewCell.swift
//  Blue
//
//  Created by 孙恩浩 on 29/01/2018.
//  Copyright © 2018 孙恩浩. All rights reserved.
//

import UIKit

class PeripheralTableViewCell: UITableViewCell {
    
    @IBOutlet weak var peripheralLabel: UILabel!
    @IBOutlet weak var rssiLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
