
import React from 'react';
import 'antd/dist/antd.css';
import { Table } from 'antd';

const List = ({ item, itemDetail, getItemDetail }) => {
    const expandedRowRender = (value) => {

        const columns = [
            { title: 'Name', dataIndex: 'store_name', key: 'name' },
            { title: 'Store Address', dataIndex: 'store_address', key: 'store_address' },
            { title: 'Item Price', dataIndex: 'item_price', key: 'item_price' },
            { title: 'Pincode', dataIndex: 'pincode', key: 'pincode' },
        ];
        return <Table columns={columns} dataSource={itemDetail} pagination={false} />;
    };

    const columns = [
        { title: 'Name', dataIndex: 'item_name', key: 'name' },
        { title: 'Price', dataIndex: 'item_price', key: 'price' },
        { title: 'Lowest Price', dataIndex: 'lowest_price', key: 'lowest_price' }
    ];

    return (
        <Table
            className="components-table-demo-nested"
            columns={columns}
            expandedRowRender={expandedRowRender}
            dataSource={item}
            pagination={false}
            style={{ background: 'linear-gradient(45deg, #97d2ff,#928DAB)' }}
            onRow={(record, rowIndex) => {
                return {
                    onClick: event => console.log(event)
                };
            }}
            onExpand={(expanded, value) => getItemDetail({ id: value.item_id })}
        />
    );
}

export default List

